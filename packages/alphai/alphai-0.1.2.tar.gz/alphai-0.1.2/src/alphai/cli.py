"""Main CLI module for alphai."""

import sys
import time
import signal
import atexit
import webbrowser
from typing import Optional
import click
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
import subprocess
import urllib.request
import urllib.error
import questionary

from .client import AlphAIClient
from .config import Config
from .auth import AuthManager
from .docker import DockerManager


console = Console()

# Global cleanup state
_cleanup_state = {
    'container_id': None,
    'tunnel_id': None,
    'project_id': None,
    'client': None,
    'docker_manager': None,
    'cleanup_done': False
}


def _get_frontend_url(api_url: str) -> str:
    """Convert API URL to frontend URL for browser opening."""
    if api_url.startswith("http://localhost") or api_url.startswith("https://localhost"):
        # For local development, assume frontend is on same host without /api
        return api_url.replace("/api", "").rstrip("/")
    elif "runalph.ai" in api_url:
        # For production, convert from runalph.ai/api to .ai
        if "/api" in api_url:
            return api_url.replace("runalph.ai/api", "runalph.ai").rstrip("/")
        else:
            return api_url.replace("runalph.ai", "runalph.ai").rstrip("/")
    else:
        # For other domains, just remove /api suffix
        return api_url.replace("/api", "").rstrip("/")


def _cleanup_handler(signum=None, frame=None):
    """Handle cleanup when script is interrupted."""
    # Check if cleanup has already been done
    if _cleanup_state['cleanup_done']:
        return
    
    # Check if there's anything to clean up
    if not any(v for k, v in _cleanup_state.items() if k != 'cleanup_done'):
        if signum is not None:  # Called by signal handler
            sys.exit(0)
        return
    
    console.print("\n[yellow]🔄 Cleaning up resources...[/yellow]")
    
    try:
        # Clean up container and cloudflared service
        if _cleanup_state['container_id'] and _cleanup_state['docker_manager']:
            _cleanup_state['docker_manager'].cleanup_container_and_tunnel(
                container_id=_cleanup_state['container_id'],
                tunnel_id=_cleanup_state['tunnel_id'],
                project_id=_cleanup_state['project_id'],
                force=True
            )
        
        # Clean up tunnel and project  
        if _cleanup_state['client'] and (_cleanup_state['tunnel_id'] or _cleanup_state['project_id']):
            _cleanup_state['client'].cleanup_tunnel_and_project(
                tunnel_id=_cleanup_state['tunnel_id'],
                project_id=_cleanup_state['project_id'],
                force=True
            )
        
        console.print("[green]✓ Cleanup completed[/green]")
        
    except Exception as e:
        console.print(f"[red]Error during cleanup: {e}[/red]")
    
    # Mark cleanup as done and reset cleanup state
    _cleanup_state.update({
        'container_id': None,
        'tunnel_id': None, 
        'project_id': None,
        'client': None,
        'docker_manager': None,
        'cleanup_done': True
    })
    
    # Only exit if called by signal handler (not by atexit)
    if signum is not None:
        sys.exit(0)


# Register cleanup handler
signal.signal(signal.SIGINT, _cleanup_handler)
signal.signal(signal.SIGTERM, _cleanup_handler)
atexit.register(_cleanup_handler)


@click.group(invoke_without_command=True)
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.option('--version', is_flag=True, help='Show version information')
@click.pass_context
def main(ctx: click.Context, debug: bool, version: bool) -> None:
    """alphai - A CLI tool for the runalph.ai platform."""
    
    if version:
        from . import __version__
        console.print(f"alphai version {__version__}")
        return
    
    # Set up context
    ctx.ensure_object(dict)
    config = Config.load()
    
    if debug:
        config.debug = True
        config.save()
    
    ctx.obj['config'] = config
    ctx.obj['client'] = AlphAIClient(config)
    
    # If no command is provided, show status
    if ctx.invoked_subcommand is None:
        ctx.obj['client'].display_status()


@main.command()
@click.option('--token', help='Bearer token for authentication')
@click.option('--api-url', help='API base URL (optional)')
@click.option('--browser', is_flag=True, help='Use browser-based authentication')
@click.option('--force', is_flag=True, help='Force re-authentication even if already logged in')
@click.pass_context
def login(ctx: click.Context, token: Optional[str], api_url: Optional[str], browser: bool, force: bool) -> None:
    """Authenticate with the runalph.ai API.
    
    If you're already authenticated, this command will validate your existing
    credentials and exit. Use --force to re-authenticate."""
    config: Config = ctx.obj['config']
    
    if api_url:
        config.api_url = api_url
    
    auth_manager = AuthManager(config)
    
    # Check if already authenticated (unless force is used or token is provided)
    if not force and not token:
        if auth_manager.check_existing_authentication():
            console.print("[green]✓ You are already logged in![/green]")
            console.print("[dim]Use 'alphai login --force' to re-authenticate or 'alphai status' to view details[/dim]")
            return
    
    if token:
        # Use provided token
        success = auth_manager.login_with_token(token)
    elif browser:
        # Use browser login
        success = auth_manager.browser_login()
    else:
        # Interactive login (will offer browser as default option)
        success = auth_manager.interactive_login()
    
    if success:
        config.save()
        console.print("[green]✓ Successfully logged in![/green]")
        
        # Test the connection
        client = AlphAIClient(config)
        if client.test_connection():
            console.print("[green]✓ Connection to API verified[/green]")
        else:
            console.print("[yellow]⚠ Warning: Could not verify API connection[/yellow]")
    else:
        console.print("[red]✗ Login failed[/red]")
        sys.exit(1)


@main.command()
@click.pass_context
def logout(ctx: click.Context) -> None:
    """Log out and clear authentication credentials."""
    config: Config = ctx.obj['config']
    
    if not config.bearer_token:
        console.print("[yellow]Already logged out[/yellow]")
        return
    
    if Confirm.ask("Are you sure you want to log out?"):
        config.clear_bearer_token()
        config.current_org = None
        config.current_project = None
        config.save()
        console.print("[green]✓ Successfully logged out[/green]")


@main.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """Show current configuration and authentication status."""
    client: AlphAIClient = ctx.obj['client']
    client.display_status()


@main.group()
@click.pass_context
def orgs(ctx: click.Context) -> None:
    """Manage organizations."""
    pass


@orgs.command('list')
@click.pass_context
def orgs_list(ctx: click.Context) -> None:
    """List all organizations."""
    client: AlphAIClient = ctx.obj['client']
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Fetching organizations...", total=None)
        orgs = client.get_organizations()
        progress.update(task, completed=1)
    
    client.display_organizations(orgs)


@orgs.command('create')
@click.option('--name', required=True, help='Organization name')
@click.option('--description', help='Organization description')
@click.pass_context
def orgs_create(ctx: click.Context, name: str, description: Optional[str]) -> None:
    """Create a new organization."""
    client: AlphAIClient = ctx.obj['client']
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Creating organization '{name}'...", total=None)
        org = client.create_organization(name, description)
        progress.update(task, completed=1)
    
    if org:
        console.print(f"[green]Organization ID: {org.get('id', 'N/A')}[/green]")


@orgs.command('select')
@click.argument('org_id')
@click.pass_context
def orgs_select(ctx: click.Context, org_id: str) -> None:
    """Select an organization as the current context."""
    config: Config = ctx.obj['config']
    config.current_org = org_id
    config.save()
    console.print(f"[green]✓ Selected organization: {org_id}[/green]")


@main.group()
@click.pass_context
def projects(ctx: click.Context) -> None:
    """Manage projects."""
    pass


@projects.command('list')
@click.option('--org', help='Organization ID to filter by')
@click.pass_context
def projects_list(ctx: click.Context, org: Optional[str]) -> None:
    """List all projects."""
    client: AlphAIClient = ctx.obj['client']
    config: Config = ctx.obj['config']
    
    # Use provided org or current org
    org_id = org or config.current_org
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Fetching projects...", total=None)
        projects = client.get_projects(org_id)
        progress.update(task, completed=1)
    
    client.display_projects(projects)


@projects.command('select')
@click.argument('project_id')
@click.pass_context
def projects_select(ctx: click.Context, project_id: str) -> None:
    """Select a project as the current context."""
    config: Config = ctx.obj['config']
    config.current_project = project_id
    config.save()
    console.print(f"[green]✓ Selected project: {project_id}[/green]")


@main.command()
#@click.option('--image', default="runalph/ai:latest", required=True, help='Docker image to run')
@click.option('--image', default="quay.io/jupyter/datascience-notebook:latest", required=True, help='Docker image to run')
@click.option('--app-port', default=5000, help='Application port (default: 5000)')
@click.option('--jupyter-port', default=8888, help='Jupyter port (default: 8888)')
@click.option('--name', help='Container name')
@click.option('--env', multiple=True, help='Environment variables (format: KEY=VALUE)')
@click.option('--volume', multiple=True, help='Volume mounts (format: HOST_PATH:CONTAINER_PATH)')
@click.option('--detach', '-d', is_flag=True, help='Run container in background')
@click.option('--local', is_flag=True, help='Run locally only (no tunnel creation)')
@click.option('--org', help='Organization slug for tunnel (interactive selection if not provided)')
@click.option('--project', help='Project name for tunnel (interactive selection if not provided)')
@click.option('--command', help='Custom command to run in container (overrides default)')
@click.option('--ensure-jupyter', is_flag=True, help='Ensure Jupyter is running (auto-start if needed)')
@click.pass_context
def run(
    ctx: click.Context,
    image: str,
    app_port: int,
    jupyter_port: int,
    name: Optional[str],
    env: tuple,
    volume: tuple,
    detach: bool,
    local: bool,
    org: Optional[str],
    project: Optional[str],
    command: Optional[str],
    ensure_jupyter: bool
) -> None:
    """Launch and manage local Docker containers with tunnel setup (default) or local-only mode."""
    config: Config = ctx.obj['config']
    client: AlphAIClient = ctx.obj['client']
    docker_manager = DockerManager(console)
    
    # Tunnel is default behavior unless --local is specified
    tunnel = not local
    
    # Validate tunnel requirements
    if tunnel:
        if not config.bearer_token:
            console.print("[red]Error: Authentication required for tunnel creation. Please run 'alphai login' first.[/red]")
            console.print("[yellow]Tip: Use --local flag to run without tunnel creation[/yellow]")
            sys.exit(1)
        
        # Interactive selection for org if not provided
        if not org:
            console.print("[yellow]No organization specified. Please select one:[/yellow]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Fetching organizations...", total=None)
                orgs_data = client.get_organizations()
                progress.update(task, completed=1)
            
            if not orgs_data or len(orgs_data) == 0:
                console.print("[red]No organizations found. Please create one first.[/red]")
                sys.exit(1)
            
            # Create choices for questionary
            org_choices = []
            for org_data in orgs_data:
                display_name = f"{org_data.name} ({org_data.slug})"
                org_choices.append(questionary.Choice(title=display_name, value=org_data.slug))
            
            # Interactive selection with arrow keys
            selected_org_slug = questionary.select(
                "Select organization (use ↑↓ arrows and press Enter):",
                choices=org_choices,
                style=questionary.Style([
                    ('question', 'bold'),
                    ('pointer', 'fg:#673ab7 bold'),
                    ('highlighted', 'fg:#673ab7 bold'),
                    ('selected', 'fg:#cc5454'),
                    ('instruction', 'fg:#888888 italic')
                ])
            ).ask()
            
            if not selected_org_slug:
                console.print("[red]No organization selected. Exiting.[/red]")
                sys.exit(1)
            
            org = selected_org_slug
            # Find the org name for display
            selected_org_name = next((o.name for o in orgs_data if o.slug == org), org)
            console.print(f"[green]✓ Selected organization: {selected_org_name} ({org})[/green]")
        
        # Interactive input for project name if not provided
        if not project:
            console.print("[yellow]No project specified. Please enter a project name:[/yellow]")
            
            # Direct project name input for run command
            while True:
                project = Prompt.ask("Enter project name")
                if project and project.strip():
                    project = project.strip()
                    console.print(f"[green]✓ Will create project: {project}[/green]")
                    break
                else:
                    console.print("[red]Project name cannot be empty[/red]")
        
        # Auto-enable ensure-jupyter for tunnel mode
        ensure_jupyter = True
    
    # Generate Jupyter token upfront if we'll need it
    jupyter_token = None
    if ensure_jupyter or tunnel:
        jupyter_token = docker_manager.generate_jupyter_token()
        console.print(f"[cyan]Generated Jupyter token: {jupyter_token[:12]}...[/cyan]")
    
    # Parse environment variables
    env_vars = {}
    for e in env:
        if '=' in e:
            key, value = e.split('=', 1)
            env_vars[key] = value
        else:
            console.print(f"[yellow]Warning: Invalid environment variable format: {e}[/yellow]")
    
    # Parse volume mounts
    volumes = {}
    for v in volume:
        if ':' in v:
            host_path, container_path = v.split(':', 1)
            volumes[host_path] = container_path
        else:
            console.print(f"[yellow]Warning: Invalid volume format: {v}[/yellow]")
    
    # Generate Jupyter startup command if needed
    startup_command = None
    if command:
        startup_command = command
    elif ensure_jupyter or tunnel:
        # When we need to control Jupyter token, always override the image's CMD/ENTRYPOINT
        # This ensures we can start Jupyter with our own token regardless of image type
        startup_command = "tail -f /dev/null"  # Keep container alive
        console.print(f"[yellow]Using keep-alive command to control Jupyter startup[/yellow]")
    else:
        # For images without custom command, keep them alive so we can interact with them
        startup_command = "tail -f /dev/null"
        console.print(f"[yellow]Keeping container alive for interactive use[/yellow]")
    
    # Start the container
    container = docker_manager.run_container(
        image=image,
        name=name,
        ports={app_port: app_port, jupyter_port: jupyter_port},
        environment=env_vars,
        volumes=volumes,
        detach=True,  # Always detach when using tunnel
        command=startup_command
    )
    
    if not container:
        console.print("[red]Failed to start container[/red]")
        sys.exit(1)
    
    console.print(f"[green]✓ Container started[/green]")
    console.print(f"[blue]Container ID: {container.id[:12]}[/blue]")
    
    # Store cleanup state for signal handling
    _cleanup_state.update({
        'container_id': container.id,
        'client': client,
        'docker_manager': docker_manager,
        'cleanup_done': False
    })
    
    # Verify container is actually running
    time.sleep(2)  # Give container a moment to start
    
    if not docker_manager.is_container_running(container.id):
        status = docker_manager.get_container_status(container.id)
        console.print(f"[red]Container failed to start or exited immediately[/red]")
        console.print(f"[red]Status: {status}[/red]")
        
        # Show container logs for debugging
        logs = docker_manager.get_container_logs(container.id, tail=20)
        if logs:
            console.print(f"[yellow]Container logs:[/yellow]")
            console.print(f"[dim]{logs}[/dim]")
        
        sys.exit(1)
    
    console.print(f"[green]✓ Container is running[/green]")
    
    # Install and ensure Jupyter is running if requested
    if ensure_jupyter:
        # Check if Jupyter is already installed
        if not _is_jupyter_installed(docker_manager, container.id):
            console.print("[yellow]Installing Jupyter in container...[/yellow]")
            if not _install_jupyter_in_container(docker_manager, container.id):
                console.print("[red]Failed to install Jupyter[/red]")
                sys.exit(1)
        else:
            console.print("[green]✓ Jupyter is already installed[/green]")
        
        # Start Jupyter with our controlled token
        success, actual_token = docker_manager.ensure_jupyter_running(
            container.id, 
            jupyter_port, 
            jupyter_token, 
            force_restart=True  # Always force restart since we overrode the entrypoint
        )
        if not success:
            console.print("[yellow]⚠ Jupyter may not be running - tunnel token extraction might fail[/yellow]")
        else:
            # Update our token if it was generated by the method
            if actual_token and not jupyter_token:
                jupyter_token = actual_token
    
    if tunnel:
        # Create tunnel
        console.print("[yellow]Creating tunnel...[/yellow]")
        
        # Create tunnel with Jupyter token
        tunnel_data = client.create_tunnel_with_project(
            org_slug=org,
            project_name=project,
            app_port=app_port,
            jupyter_port=jupyter_port,
            jupyter_token=jupyter_token
        )
        
        if not tunnel_data:
            console.print("[red]Failed to create tunnel[/red]")
            sys.exit(1)
        
        # Store tunnel and project IDs for cleanup
        _cleanup_state.update({
            'tunnel_id': tunnel_data.id,
            'project_id': tunnel_data.project_data.id if tunnel_data.project_data and hasattr(tunnel_data.project_data, 'id') else None
        })
        
        # Check if cloudflared is already installed, install if needed
        if not _is_cloudflared_installed(docker_manager, container.id):
            console.print("[yellow]Installing cloudflared in container...[/yellow]")
            if not docker_manager.install_cloudflared_in_container(container.id):
                console.print("[yellow]Warning: cloudflared installation failed, but container is running[/yellow]")
                return
        else:
            console.print("[green]✓ cloudflared is already installed[/green]")
        
        # Set up tunnel service using the cloudflared token
        cloudflared_token = tunnel_data.cloudflared_token if hasattr(tunnel_data, 'cloudflared_token') else tunnel_data.cloudflared_token
        if docker_manager.setup_tunnel_in_container(container.id, cloudflared_token):
            console.print("\n[bold green]🎉 Container with tunnel setup complete![/bold green]")
            
            # Create a nice summary panel
            summary_content = []
            summary_content.append(f"[bold]Container ID:[/bold] {container.id[:12]}")
            summary_content.append(f"[bold]Tunnel ID:[/bold] {tunnel_data.id}")
            summary_content.append("")
            summary_content.append("[bold blue]Local Access:[/bold blue]")
            summary_content.append(f"  • App: http://localhost:{app_port}")
            if jupyter_token:
                summary_content.append(f"  • Jupyter: http://localhost:{jupyter_port}?token={jupyter_token}")
            else:
                summary_content.append(f"  • Jupyter: http://localhost:{jupyter_port}")
            summary_content.append("")
            summary_content.append("[bold green]Public Access:[/bold green]")
            summary_content.append(f"  • App: {tunnel_data.app_url}")
            if jupyter_token:
                summary_content.append(f"  • Jupyter: {tunnel_data.jupyter_url}?token={jupyter_token}")
            else:
                summary_content.append(f"  • Jupyter: {tunnel_data.jupyter_url}")
            summary_content.append("")
            if jupyter_token:
                summary_content.append("[bold cyan]Jupyter Token:[/bold cyan]")
                summary_content.append(f"  {jupyter_token}")
                summary_content.append("")
            summary_content.append("[bold yellow]Management:[/bold yellow]")
            summary_content.append(f"  • Stop container: docker stop {container.id[:12]}")
            summary_content.append(f"  • View logs: docker logs {container.id[:12]}")
            summary_content.append(f"  • Delete tunnel: alphai tunnels delete {tunnel_data.id}")
            summary_content.append(f"  • Full cleanup: alphai cleanup {container.id[:12]} --tunnel-id {tunnel_data.id}")
            summary_content.append("")
            summary_content.append("[bold cyan]Quick Cleanup:[/bold cyan]")
            summary_content.append("  • Press Ctrl+C to automatically cleanup all resources")
            
            panel = Panel(
                "\n".join(summary_content),
                title="🚀 Deployment Summary",
                title_align="left",
                border_style="green"
            )
            console.print(panel)
            
            # Wait for tunnel URLs to become available
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Waiting for tunnel URLs to become available...", total=None)
                #_wait_for_tunnel_ready(tunnel_data)
                time.sleep(5)
                progress.update(task, completed=1)
            
            # Open browser to the project page
            frontend_url = _get_frontend_url(config.api_url)
            project_url = f"{frontend_url}/{org}/{project}"
            console.print(f"\n[cyan]🌐 Opening browser to: {project_url}[/cyan]")
            try:
                webbrowser.open(project_url)
            except Exception as e:
                console.print(f"[yellow]Warning: Could not open browser automatically: {e}[/yellow]")
                console.print(f"[yellow]Please manually visit: {project_url}[/yellow]")
        else:
            console.print("[yellow]Warning: Tunnel service setup failed, but container is running[/yellow]")
    else:
        # Non-tunnel mode - just display local URLs
        console.print(f"[blue]Application: http://localhost:{app_port}[/blue]")
        if jupyter_token:
            console.print(f"[blue]Jupyter: http://localhost:{jupyter_port}?token={jupyter_token}[/blue]")
            console.print(f"[dim]Jupyter Token: {jupyter_token}[/dim]")
        else:
            console.print(f"[blue]Jupyter: http://localhost:{jupyter_port}[/blue]")
            console.print(f"[dim]Check container logs for Jupyter token: docker logs {container.id[:12]}[/dim]")
        
        console.print(f"\n[bold yellow]Cleanup:[/bold yellow]")
        console.print(f"  • Stop container: docker stop {container.id[:12]}")
        console.print(f"  • Quick cleanup: alphai cleanup {container.id[:12]}")
        console.print(f"  • Press Ctrl+C to automatically stop and remove container")
        
        if not detach:
            console.print(f"[dim]Container is running in background. Use 'docker logs {container.id[:12]}' to view logs.[/dim]")
    
    # Keep the process running and wait for Ctrl+C for cleanup
    try:
        console.print(f"\n[bold green]🎯 Container is running! Press Ctrl+C to cleanup all resources.[/bold green]")
        # Keep the main process alive to handle signals
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Signal handler will take care of cleanup and exit
        pass


def _wait_for_tunnel_ready(tunnel_data, timeout_seconds: int = 30) -> bool:
    """Wait for Jupyter tunnel URL to become available."""
    import time
    import urllib.request
    import urllib.error
    
    jupyter_url = tunnel_data.jupyter_url
    console.print(f"[yellow]🔄 Checking if {jupyter_url} is ready...[/yellow]")
    
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        try:
            # Simple HEAD request with short timeout
            req = urllib.request.Request(jupyter_url)
            with urllib.request.urlopen(req, timeout=5) as response:
                console.print(f"[green]✅ Jupyter tunnel is ready! ({response.status})[/green]")
                time.sleep(2)
                return True
        except (urllib.error.URLError, urllib.error.HTTPError, OSError):
            # Any response (even errors) means the route exists
            pass
        except Exception:
            # Still not ready, continue waiting
            pass
        
        time.sleep(2)
    
    console.print(f"[yellow]⚠ Tunnel check timed out after {timeout_seconds}s[/yellow]")
    return False


def _is_jupyter_installed(docker_manager, container_id: str) -> bool:
    """Check if Jupyter is actually installed in the container."""
    try:
        # Try to check if jupyter command exists
        result = subprocess.run(
            ["docker", "exec", container_id, "which", "jupyter"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return True
        
        # Also try checking for jupyter-lab specifically
        result = subprocess.run(
            ["docker", "exec", container_id, "which", "jupyter-lab"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return result.returncode == 0
        
    except Exception as e:
        console.print(f"[yellow]Warning: Could not check Jupyter installation: {e}[/yellow]")
        return False


def _is_cloudflared_installed(docker_manager, container_id: str) -> bool:
    """Check if cloudflared is actually installed in the container."""
    try:
        # Try to check if cloudflared command exists
        result = subprocess.run(
            ["docker", "exec", container_id, "which", "cloudflared"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return result.returncode == 0
        
    except Exception as e:
        console.print(f"[yellow]Warning: Could not check cloudflared installation: {e}[/yellow]")
        return False


def _install_jupyter_in_container(docker_manager, container_id: str) -> bool:
    """Install Jupyter in a container that doesn't have it."""
    # Detect package manager
    package_manager = docker_manager._detect_package_manager(container_id)
    
    if not package_manager:
        console.print("[red]Could not detect package manager for Jupyter installation[/red]")
        return False
    
    try:
        if package_manager in ['apt', 'apt-get']:
            install_commands = [
                "apt-get update",
                "apt-get install -y python3-pip",
                "pip3 install jupyter jupyterlab"
            ]
        elif package_manager in ['yum', 'dnf']:
            install_commands = [
                f"{package_manager} update -y",
                f"{package_manager} install -y python3-pip",
                "pip3 install jupyter jupyterlab"
            ]
        elif package_manager == 'apk':
            install_commands = [
                "apk update",
                "apk add --no-cache python3 py3-pip",
                "pip3 install jupyter jupyterlab"
            ]
        else:
            # Try generic approach
            install_commands = [
                "pip3 install jupyter jupyterlab"
            ]
        
        for cmd in install_commands:
            result = subprocess.run(
                ["docker", "exec", "--user", "root", container_id, "bash", "-c", cmd],
                capture_output=True,
                text=True,
                timeout=120  # Longer timeout for installations
            )
            
            if result.returncode != 0:
                console.print(f"[red]Failed to run: {cmd}[/red]")
                console.print(f"[red]Error: {result.stderr}[/red]")
                return False
        
        console.print("[green]✓ Jupyter installed successfully[/green]")
        return True
        
    except Exception as e:
        console.print(f"[red]Error installing Jupyter: {e}[/red]")
        return False


@main.group()
@click.pass_context
def tunnels(ctx: click.Context) -> None:
    """Manage tunnels."""
    pass


@tunnels.command('create')
@click.option('--org', required=True, help='Organization slug')
@click.option('--project', required=True, help='Project name')
@click.option('--app-port', default=5000, help='Application port (default: 5000)')
@click.option('--jupyter-port', default=8888, help='Jupyter port (default: 8888)')
@click.option('--project-only', is_flag=True, help='Create project only, skip tunnel creation')
@click.pass_context
def tunnels_create(
    ctx: click.Context, 
    org: str, 
    project: str, 
    app_port: int, 
    jupyter_port: int,
    project_only: bool
) -> None:
    """Create a new tunnel and associated project."""
    client: AlphAIClient = ctx.obj['client']
    
    if project_only:
        # Create project only
        org_data = client.get_organization_by_slug(org)
        if not org_data:
            console.print(f"[red]Organization with slug '{org}' not found[/red]")
            sys.exit(1)
        
        project_data = client.create_project(
            name=project,
            organization_id=org_data.id,
            port=app_port
        )
        
        if project_data:
            console.print(f"[green]✓ Project '{project}' created successfully[/green]")
    else:
        # Create tunnel and project
        tunnel_data = client.create_tunnel_with_project(
            org_slug=org,
            project_name=project,
            app_port=app_port,
            jupyter_port=jupyter_port
        )
        
        if tunnel_data:
            console.print(f"\n[bold]Manual Setup Command:[/bold]")
            cloudflared_token = tunnel_data.cloudflared_token if hasattr(tunnel_data, 'cloudflared_token') else tunnel_data.token
            console.print(f"[green]cloudflared service install {cloudflared_token}[/green]")
            console.print(f"\n[dim]Copy the above command to set up cloudflared manually in your container[/dim]")
            console.print(f"[dim]Note: Add Jupyter token to project after starting your container[/dim]")


@tunnels.command('get')
@click.argument('tunnel_id')
@click.pass_context
def tunnels_get(ctx: click.Context, tunnel_id: str) -> None:
    """Get tunnel information."""
    client: AlphAIClient = ctx.obj['client']
    
    tunnel_data = client.get_tunnel(tunnel_id)
    if tunnel_data:
        console.print(f"[bold]Tunnel ID:[/bold] {tunnel_data.id}")
        console.print(f"[bold]Name:[/bold] {tunnel_data.name}")
        console.print(f"[bold]App URL:[/bold] {tunnel_data.app_url}")
        console.print(f"[bold]Jupyter URL:[/bold] {tunnel_data.jupyter_url}")
        console.print(f"[bold]Created:[/bold] {tunnel_data.created_at}")
    else:
        console.print("[red]Tunnel not found[/red]")


@tunnels.command('delete')
@click.argument('tunnel_id')
@click.option('--force', is_flag=True, help='Skip confirmation')
@click.pass_context
def tunnels_delete(ctx: click.Context, tunnel_id: str, force: bool) -> None:
    """Delete a tunnel."""
    client: AlphAIClient = ctx.obj['client']
    
    if not force:
        if not Confirm.ask(f"Are you sure you want to delete tunnel {tunnel_id}?"):
            console.print("[yellow]Cancelled[/yellow]")
            return
    
    client.delete_tunnel(tunnel_id)


@main.command()
@click.argument('container_id')
@click.option('--tunnel-id', help='Tunnel ID to delete')
@click.option('--project-id', help='Project ID to delete')
@click.option('--force', is_flag=True, help='Skip confirmation and force cleanup')
@click.option('--containers-only', is_flag=True, help='Only cleanup container and cloudflared service, skip tunnel/project deletion')
@click.pass_context
def cleanup(
    ctx: click.Context, 
    container_id: str, 
    tunnel_id: Optional[str], 
    project_id: Optional[str],
    force: bool,
    containers_only: bool
) -> None:
    """Clean up containers, tunnels, and projects created by alphai run.
    
    This command performs comprehensive cleanup by:
    1. Uninstalling cloudflared service from the container
    2. Stopping and removing the Docker container
    3. Deleting the tunnel (unless --containers-only is used)
    4. Deleting the project (unless --containers-only is used)
    
    Note: Project deletion has SDK limitations and may require manual cleanup
    via the web interface for specific project IDs.
    
    Examples:
      alphai cleanup abc123456789                    # Container only
      alphai cleanup abc123456789 --tunnel-id xyz   # Container + tunnel
      alphai cleanup abc123456789 --force           # Skip confirmations
    """
    config: Config = ctx.obj['config']
    client: AlphAIClient = ctx.obj['client']
    docker_manager = DockerManager(console)
    
    # Confirmation unless force is used
    if not force:
        cleanup_items = [f"Container {container_id[:12]}"]
        if tunnel_id and not containers_only:
            cleanup_items.append(f"Tunnel {tunnel_id}")
        if project_id and not containers_only:
            cleanup_items.append(f"Project {project_id}")
        
        console.print(f"[yellow]Will cleanup: {', '.join(cleanup_items)}[/yellow]")
        if not Confirm.ask("Continue with cleanup?"):
            console.print("[yellow]Cancelled[/yellow]")
            return
    
    console.print("[bold]🔄 Starting cleanup process...[/bold]")
    
    # Step 1: Container and cloudflared cleanup
    success = docker_manager.cleanup_container_and_tunnel(
        container_id=container_id,
        tunnel_id=tunnel_id,
        project_id=project_id,
        force=force
    )
    
    # Step 2: API cleanup (unless containers-only)
    if not containers_only and (tunnel_id or project_id):
        if not config.bearer_token:
            console.print("[yellow]Warning: No authentication token - skipping tunnel/project cleanup[/yellow]")
            console.print("[dim]Run 'alphai login' to enable tunnel/project cleanup[/dim]")
        else:
            api_success = client.cleanup_tunnel_and_project(
                tunnel_id=tunnel_id,
                project_id=project_id,
                force=force
            )
            success = success and api_success
    
    # Summary
    if success:
        console.print("\n[bold green]✅ Cleanup completed successfully![/bold green]")
    else:
        console.print("\n[bold yellow]⚠ Cleanup completed with warnings[/bold yellow]")
        console.print("[dim]Check the output above for details[/dim]")


@main.group()
@click.pass_context
def config(ctx: click.Context) -> None:
    """Manage configuration settings."""
    pass


@config.command('show')
@click.pass_context
def config_show(ctx: click.Context) -> None:
    """Show current configuration."""
    client: AlphAIClient = ctx.obj['client']
    client.display_status()


@config.command('set')
@click.argument('key')
@click.argument('value')
@click.pass_context
def config_set(ctx: click.Context, key: str, value: str) -> None:
    """Set a configuration value."""
    config: Config = ctx.obj['config']
    
    valid_keys = {'api_url', 'debug', 'current_org', 'current_project'}
    
    if key not in valid_keys:
        console.print(f"[red]Invalid configuration key. Valid keys: {', '.join(valid_keys)}[/red]")
        sys.exit(1)
    
    # Convert string values to appropriate types
    if key == 'debug':
        value = value.lower() in ('true', '1', 'yes', 'on')
    
    setattr(config, key, value)
    config.save()
    console.print(f"[green]✓ Set {key} = {value}[/green]")


@config.command('reset')
@click.pass_context
def config_reset(ctx: click.Context) -> None:
    """Reset configuration to defaults."""
    if Confirm.ask("Are you sure you want to reset all configuration to defaults?"):
        config_file = Config.get_config_file()
        if config_file.exists():
            config_file.unlink()
        
        # Clear keyring
        config = Config()
        config.clear_bearer_token()
        
        console.print("[green]✓ Configuration reset to defaults[/green]")


if __name__ == '__main__':
    main() 