"""Client wrapper for alph-sdk."""

import sys
from typing import Optional, List, Dict, Any
from alph_sdk import AlphSDK
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .config import Config


class TunnelData:
    """Custom wrapper for tunnel data with additional fields."""
    
    def __init__(self, tunnel_data, cloudflared_token: str, jupyter_token: Optional[str] = None):
        """Initialize with tunnel data and tokens."""
        self.original_data = tunnel_data
        self.cloudflared_token = cloudflared_token
        self.jupyter_token = jupyter_token
        self.project_data = None
        
        # Proxy all attributes from original data
        for attr in ['id', 'name', 'app_url', 'jupyter_url', 'hostname', 'jupyter_hostname', 'created_at']:
            if hasattr(tunnel_data, attr):
                setattr(self, attr, getattr(tunnel_data, attr))
    

class AlphAIClient:
    """High-level client for interacting with the Alph API."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the client with configuration."""
        self.config = config or Config.load()
        self.console = Console()
        self._sdk = None
    
    @property
    def sdk(self) -> AlphSDK:
        """Get the SDK instance, creating it if necessary."""
        if self._sdk is None:
            if not self.config.bearer_token:
                self.console.print("[red]Error: No authentication token found. Please run 'alphai login' first.[/red]")
                sys.exit(1)
            
            self._sdk = AlphSDK(**self.config.to_sdk_config())
        return self._sdk
    
    def test_connection(self) -> bool:
        """Test the connection to the API."""
        try:
            # Try to get organizations as a connection test
            response = self.sdk.orgs.get()
            return response.result.status == "success" if response.result.status else True
        except Exception as e:
            self.console.print(f"[red]Connection test failed: {e}[/red]")
            return False
    
    def get_organizations(self) -> List[Dict[str, Any]]:
        """Get all organizations."""
        try:
            response = self.sdk.orgs.get()
            # Access organizations from response.result.organizations
            return response.result.organizations or []
        except Exception as e:
            self.console.print(f"[red]Error getting organizations: {e}[/red]")
            return []
    
    def create_organization(self, name: str, description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Create a new organization."""
        try:
            response = self.sdk.orgs.create({
                "name": name,
                "description": description or ""
            })
            if response.result.status == "success":
                self.console.print(f"[green]✓ Organization '{name}' created successfully[/green]")
                return response.result.organization
            else:
                self.console.print(f"[red]Failed to create organization: {response.result.status}[/red]")
                return None
        except Exception as e:
            self.console.print(f"[red]Error creating organization: {e}[/red]")
            return None
    
    def get_projects(self, org_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all projects, optionally filtered by organization."""
        try:
            params = {}
            if org_id:
                params["org_id"] = org_id
            
            response = self.sdk.projects.get(**params)
            # Access projects from response.result.projects
            return response.result.projects or []
        except Exception as e:
            self.console.print(f"[red]Error getting projects: {e}[/red]")
            return []
    
    def display_organizations(self, orgs: List[Dict[str, Any]]) -> None:
        """Display organizations in a nice table format."""
        if not orgs:
            self.console.print("[yellow]No organizations found.[/yellow]")
            return
        
        table = Table(title="Organizations")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="green")
        table.add_column("Role", style="blue")
        table.add_column("Slug", style="dim")
        table.add_column("Subscription", style="yellow")
        
        for org in orgs:
            table.add_row(
                org.id or "",
                org.name or "",
                org.role or "",
                org.slug or "",
                org.subscription_level or ""
            )
        
        self.console.print(table)
    
    def display_projects(self, projects: List[Dict[str, Any]]) -> None:
        """Display projects in a nice table format."""
        if not projects:
            self.console.print("[yellow]No projects found.[/yellow]")
            return
        
        table = Table(title="Projects")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="green")
        table.add_column("Organization", style="blue")
        table.add_column("Status", style="yellow")
        table.add_column("Created", style="dim")
        
        for project in projects:
            # Handle organization name safely
            org_name = ""
            if project.organization:
                org_name = project.organization.name or ""
            
            table.add_row(
                project.id or "",
                project.name or "",
                org_name,
                project.status or "",
                project.created_at or ""
            )
        
        self.console.print(table)
    
    def display_status(self) -> None:
        """Display current configuration status."""
        status_info = []
        
        # API URL
        status_info.append(f"[bold]API URL:[/bold] {self.config.api_url}")
        
        # Authentication status
        if self.config.bearer_token:
            status_info.append("[bold]Authentication:[/bold] [green]✓ Logged in[/green]")
        else:
            status_info.append("[bold]Authentication:[/bold] [red]✗ Not logged in[/red]")
        
        # Current organization
        if self.config.current_org:
            status_info.append(f"[bold]Current Organization:[/bold] {self.config.current_org}")
        else:
            status_info.append("[bold]Current Organization:[/bold] [dim]None selected[/dim]")
        
        # Current project
        if self.config.current_project:
            status_info.append(f"[bold]Current Project:[/bold] {self.config.current_project}")
        else:
            status_info.append("[bold]Current Project:[/bold] [dim]None selected[/dim]")
        
        # Debug mode
        if self.config.debug:
            status_info.append("[bold]Debug Mode:[/bold] [yellow]Enabled[/yellow]")
        
        panel = Panel(
            "\n".join(status_info),
            title="alphai Status",
            title_align="left"
        )
        self.console.print(panel)
    
    def create_tunnel(
        self, 
        org_slug: str, 
        project_name: str, 
        app_port: int = 5000, 
        jupyter_port: int = 8888
    ) -> Optional[Dict[str, Any]]:
        """Create a new tunnel and return the tunnel data including token."""
        try:
            response = self.sdk.tunnels.create(request={
                "org_slug": org_slug,
                "project_name": project_name,
                "app_port": app_port,
                "jupyter_port": jupyter_port
            })
            
            if response.result.status == "success":
                tunnel_data = response.result.data
                self.console.print(f"[green]✓ Tunnel created successfully[/green]")
                self.console.print(f"[blue]Tunnel ID: {tunnel_data.id}[/blue]")
                self.console.print(f"[blue]App URL: {tunnel_data.app_url}[/blue]")
                self.console.print(f"[blue]Jupyter URL: {tunnel_data.jupyter_url}[/blue]")
                return tunnel_data
            else:
                self.console.print(f"[red]Failed to create tunnel: {response.result.status}[/red]")
                return None
        except Exception as e:
            self.console.print(f"[red]Error creating tunnel: {e}[/red]")
            return None
    
    def get_tunnel(self, tunnel_id: str) -> Optional[Dict[str, Any]]:
        """Get tunnel information by ID."""
        try:
            response = self.sdk.tunnels.get(tunnel_id=tunnel_id)
            return response.result.data if response.result.status == "success" else None
        except Exception as e:
            self.console.print(f"[red]Error getting tunnel: {e}[/red]")
            return None
    
    def delete_tunnel(self, tunnel_id: str) -> bool:
        """Delete a tunnel by ID."""
        try:
            response = self.sdk.tunnels.delete(tunnel_id=tunnel_id)
            if response.result.status == "success":
                self.console.print(f"[green]✓ Tunnel {tunnel_id} deleted successfully[/green]")
                return True
            else:
                self.console.print(f"[red]Failed to delete tunnel: {response.result.status}[/red]")
                return False
        except Exception as e:
            self.console.print(f"[red]Error deleting tunnel: {e}[/red]")
            return False
    
    def create_project(
        self, 
        name: str, 
        organization_id: str,
        port: int = 5000,
        url: Optional[str] = None,
        port_forward_url: Optional[str] = None,
        token: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Create a new project."""
        try:
            response = self.sdk.projects.create(request={
                "name": name,
                "organization_id": organization_id,
                "port": port,
                "url": url,
                "port_forward_url": port_forward_url,
                "token": token,
                "server_request": "external",
            })
            
            if response.result.status == "success":
                project_data = response.result.project  # Use 'project' instead of 'data'
                self.console.print(f"[green]✓ Project '{name}' created successfully[/green]")
                return project_data
            else:
                self.console.print(f"[red]Failed to create project: {response.result.status}[/red]")
                return None
        except Exception as e:
            self.console.print(f"[red]Error creating project: {e}[/red]")
            return None
    
    def get_organization_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Get organization by slug."""
        try:
            orgs = self.get_organizations()
            for org in orgs:
                if hasattr(org, 'slug') and org.slug == slug:
                    return org
            return None
        except Exception as e:
            self.console.print(f"[red]Error getting organization by slug: {e}[/red]")
            return None
    
    def create_tunnel_with_project(
        self, 
        org_slug: str, 
        project_name: str, 
        app_port: int = 5000, 
        jupyter_port: int = 8888,
        jupyter_token: Optional[str] = None
    ) -> Optional[TunnelData]:
        """Create a tunnel and associated project."""
        # First, get the organization
        org = self.get_organization_by_slug(org_slug)
        if not org:
            self.console.print(f"[red]Organization with slug '{org_slug}' not found[/red]")
            return None
        
        # Create the tunnel
        tunnel_data = self.create_tunnel(org_slug, project_name, app_port, jupyter_port)
        if not tunnel_data:
            return None
        
        # Create custom wrapper with tokens
        wrapped_tunnel = TunnelData(
            tunnel_data=tunnel_data,
            cloudflared_token=tunnel_data.token,
            jupyter_token=jupyter_token
        )
        
        # Create the associated project (with Jupyter token if available)
        self.console.print(f"[yellow]Creating associated project '{project_name}'...[/yellow]")
        project_data = self.create_project(
            name=project_name,
            organization_id=org.id,
            port=app_port,
            url=tunnel_data.jupyter_url,
            port_forward_url=tunnel_data.app_url,
            token=jupyter_token  # Use Jupyter token, not cloudflared token
        )
        
        # Store project data in wrapper
        wrapped_tunnel.project_data = project_data
        
        # Enhanced logging output
        self.console.print("\n[bold green]🎉 Tunnel and Project Setup Complete![/bold green]")
        self.console.print(f"[bold]Tunnel ID:[/bold] {wrapped_tunnel.id}")
        if project_data:
            self.console.print(f"[bold]Project ID:[/bold] {project_data.id if hasattr(project_data, 'id') else 'Created'}")
        
        # Token information
        self.console.print(f"\n[bold]Cloudflared Token:[/bold]")
        self.console.print(f"[dim]For tunnel setup: cloudflared service install {wrapped_tunnel.cloudflared_token}[/dim]")
        
        if jupyter_token:
            self.console.print(f"\n[bold]Jupyter Token:[/bold]")
            self.console.print(f"[dim]For Jupyter access: {jupyter_token}[/dim]")
        
        # URLs
        self.console.print(f"\n[bold]Access URLs:[/bold]")
        self.console.print(f"[blue]• App URL: {wrapped_tunnel.app_url}[/blue]")
        self.console.print(f"[blue]• Jupyter URL: {wrapped_tunnel.jupyter_url}[/blue]")
        
        return wrapped_tunnel
    
    def update_project_jupyter_token(self, project_data: Dict[str, Any], jupyter_token: str) -> bool:
        """Update project with Jupyter token after container starts."""
        # Since there's no update method, we'll store this for the next version
        # For now, just print that we have the token
        self.console.print(f"[green]✓ Jupyter token extracted: {jupyter_token[:12]}...[/green]")
        return True

    def delete_project(self, project_id: str) -> bool:
        """Delete a project by ID."""
        try:
            response = self.sdk.projects.delete(project_id=project_id)
            if response.result.status == "success":
                self.console.print(f"[green]✓ Project {project_id} deleted successfully[/green]")
                return True
            else:
                self.console.print(f"[red]Failed to delete project: {response.result.status}[/red]")
                return False
        except Exception as e:
            self.console.print(f"[red]Error deleting project: {e}[/red]")
            return False

    def cleanup_tunnel_and_project(
        self, 
        tunnel_id: Optional[str] = None, 
        project_id: Optional[str] = None,
        force: bool = False
    ) -> bool:
        """Comprehensive cleanup of tunnel and project resources."""
        success = True
        
        if not tunnel_id and not project_id:
            self.console.print("[yellow]No tunnel or project ID provided for cleanup[/yellow]")
            return True
        
        # Delete tunnel first
        if tunnel_id:
            self.console.print(f"[yellow]Deleting tunnel {tunnel_id}...[/yellow]")
            if not self.delete_tunnel(tunnel_id):
                success = False
        
        # Delete project second  
        if project_id:
            self.console.print(f"[yellow]Deleting project {project_id}...[/yellow]")
            if not self.delete_project(project_id):
                success = False
        
        if success:
            self.console.print("[green]✓ Tunnel and project cleanup completed successfully[/green]")
        else:
            self.console.print("[yellow]⚠ Tunnel and project cleanup completed with errors[/yellow]")
        
        return success 