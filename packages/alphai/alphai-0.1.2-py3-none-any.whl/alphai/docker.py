"""Docker management for alphai CLI."""

import sys
from typing import Optional, Dict, Any, List
import subprocess
import shutil
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel


class DockerManager:
    """Manage Docker operations for the alphai CLI."""
    
    def __init__(self, console: Console):
        """Initialize the Docker manager."""
        self.console = console
        self._docker_available = None
    
    def is_docker_available(self) -> bool:
        """Check if Docker is available and running."""
        if self._docker_available is not None:
            return self._docker_available
        
        # Check if docker command exists
        if not shutil.which("docker"):
            self._docker_available = False
            return False
        
        # Check if Docker daemon is running
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                text=True,
                timeout=10
            )
            self._docker_available = result.returncode == 0
            return self._docker_available
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            self._docker_available = False
            return False
    
    def pull_image(self, image: str) -> bool:
        """Pull a Docker image."""
        if not self.is_docker_available():
            self.console.print("[red]Error: Docker is not available or not running[/red]")
            return False
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task(f"Pulling image {image}...", total=None)
                
                result = subprocess.run(
                    ["docker", "pull", image],
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minutes timeout
                )
                
                progress.update(task, completed=1)
            
            if result.returncode == 0:
                self.console.print(f"[green]✓ Successfully pulled image {image}[/green]")
                return True
            else:
                self.console.print(f"[red]Error pulling image {image}: {result.stderr}[/red]")
                return False
                
        except subprocess.TimeoutExpired:
            self.console.print(f"[red]Timeout pulling image {image}[/red]")
            return False
        except Exception as e:
            self.console.print(f"[red]Error pulling image {image}: {e}[/red]")
            return False
    
    def run_container(
        self,
        image: str,
        name: Optional[str] = None,
        ports: Optional[Dict[int, int]] = None,
        environment: Optional[Dict[str, str]] = None,
        volumes: Optional[Dict[str, str]] = None,
        detach: bool = False,
        command: Optional[str] = None
    ) -> Optional[Any]:
        """Run a Docker container with the specified configuration."""
        if not self.is_docker_available():
            self.console.print("[red]Error: Docker is not available or not running[/red]")
            self.console.print("[yellow]Please install Docker and ensure it's running[/yellow]")
            return None
        
        # Build docker run command
        cmd = ["docker", "run"]
        
        # Add name if specified
        if name:
            cmd.extend(["--name", name])
        
        # Add port mappings
        if ports:
            for host_port, container_port in ports.items():
                cmd.extend(["-p", f"{host_port}:{container_port}"])
        
        # Add environment variables
        if environment:
            for key, value in environment.items():
                cmd.extend(["-e", f"{key}={value}"])
        
        # Add volume mounts
        if volumes:
            for host_path, container_path in volumes.items():
                cmd.extend(["-v", f"{host_path}:{container_path}"])
        
        # Add detach flag
        if detach:
            cmd.append("-d")
        else:
            cmd.extend(["-it"])
        
        # Remove container when it exits (unless detached)
        if not detach:
            cmd.append("--rm")
        
        # Add the image
        cmd.append(image)
        
        # Add custom command if specified
        if command:
            cmd.extend(["bash", "-c", command])
        
        try:
            # Check if image exists locally, pull if not
            check_result = subprocess.run(
                ["docker", "images", "-q", image],
                capture_output=True,
                text=True
            )
            
            if not check_result.stdout.strip():
                self.console.print(f"[yellow]Image {image} not found locally, pulling...[/yellow]")
                if not self.pull_image(image):
                    return None
            
            # Run the container
            if detach:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=self.console
                ) as progress:
                    task = progress.add_task("Starting container...", total=None)
                    
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    progress.update(task, completed=1)
                
                if result.returncode == 0:
                    container_id = result.stdout.strip()
                    return MockContainer(container_id)
                else:
                    self.console.print(f"[red]Error starting container: {result.stderr}[/red]")
                    return None
            else:
                # Interactive mode
                self.console.print(f"[green]Starting interactive container from {image}...[/green]")
                self.console.print("[dim]Press Ctrl+C to stop the container[/dim]")
                
                try:
                    # Run interactively without capturing output
                    result = subprocess.run(cmd)
                    return MockContainer("interactive")
                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Container stopped by user[/yellow]")
                    return MockContainer("interactive")
                
        except subprocess.TimeoutExpired:
            self.console.print("[red]Timeout starting container[/red]")
            return None
        except Exception as e:
            self.console.print(f"[red]Error running container: {e}[/red]")
            return None
    
    def list_containers(self, all_containers: bool = False) -> list:
        """List Docker containers."""
        if not self.is_docker_available():
            return []
        
        try:
            cmd = ["docker", "ps"]
            if all_containers:
                cmd.append("-a")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Parse output (this is a simplified version)
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    return lines[1:]  # Skip header
                return []
            else:
                return []
                
        except Exception:
            return []
    
    def stop_container(self, container_id: str) -> bool:
        """Stop a running container."""
        if not self.is_docker_available():
            return False
        
        try:
            result = subprocess.run(
                ["docker", "stop", container_id],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return result.returncode == 0
            
        except Exception:
            return False
    
    def remove_container(self, container_id: str, force: bool = False) -> bool:
        """Remove a container."""
        if not self.is_docker_available():
            return False
        
        try:
            cmd = ["docker", "rm"]
            if force:
                cmd.append("-f")
            cmd.append(container_id)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return result.returncode == 0
            
        except Exception:
            return False
    
    def install_cloudflared_in_container(self, container_id: str) -> bool:
        """Install cloudflared in a running container."""
        if not self.is_docker_available():
            return False
        
        try:
            # Detect the container's package manager and architecture
            package_manager = self._detect_package_manager(container_id)
            architecture = self._detect_architecture(container_id)
            
            if not package_manager:
                self.console.print("[red]Unsupported container: No compatible package manager found[/red]")
                return False
            
            # Commands to install cloudflared based on package manager
            install_commands = self._get_install_commands(package_manager, architecture)
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("Installing cloudflared in container...", total=len(install_commands))
                
                for i, command in enumerate(install_commands):
                    result = subprocess.run(
                        ["docker", "exec", "--user", "root", container_id, "bash", "-c", command],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    
                    if result.returncode != 0:
                        self.console.print(f"[red]Error running command '{command}': {result.stderr}[/red]")
                        return False
                    
                    progress.update(task, advance=1)
            
            self.console.print("[green]✓ cloudflared installed successfully[/green]")
            return True
            
        except subprocess.TimeoutExpired:
            self.console.print("[red]Timeout installing cloudflared[/red]")
            return False
        except Exception as e:
            self.console.print(f"[red]Error installing cloudflared: {e}[/red]")
            return False
    
    def _detect_package_manager(self, container_id: str) -> Optional[str]:
        """Detect the package manager available in the container."""
        package_managers = {
            'apt': 'which apt',
            'apt-get': 'which apt-get',
            'yum': 'which yum',
            'dnf': 'which dnf',
            'apk': 'which apk',
            'zypper': 'which zypper'
        }
        
        for pm_name, check_cmd in package_managers.items():
            try:
                result = subprocess.run(
                    ["docker", "exec", container_id, "bash", "-c", check_cmd],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    return pm_name
            except:
                continue
        
        return None
    
    def _detect_architecture(self, container_id: str) -> str:
        """Detect the container's architecture."""
        try:
            result = subprocess.run(
                ["docker", "exec", container_id, "uname", "-m"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                arch = result.stdout.strip()
                # Map to cloudflared architecture names
                arch_map = {
                    'x86_64': 'amd64',
                    'aarch64': 'arm64',
                    'armv7l': 'arm',
                    'i386': '386'
                }
                return arch_map.get(arch, 'amd64')
        except:
            pass
        
        return 'amd64'  # Default fallback
    
    def _get_install_commands(self, package_manager: str, architecture: str) -> List[str]:
        """Get installation commands based on package manager and architecture."""
        cloudflared_url = f"https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-{architecture}"
        
        if package_manager == 'apt-get':
            return [
                "apt-get update",
                "apt-get install -y wget",
                f"wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-{architecture}.deb",
                f"dpkg -i cloudflared-linux-{architecture}.deb",
                f"rm cloudflared-linux-{architecture}.deb"
            ]
        
        elif package_manager in ['yum', 'dnf']:
            return [
                f"{package_manager} update -y",
                f"{package_manager} install -y wget",
                f"wget -q {cloudflared_url} -O /usr/local/bin/cloudflared",
                "chmod +x /usr/local/bin/cloudflared"
            ]
        
        elif package_manager == 'apk':
            return [
                "apk update",
                "apk add --no-cache wget",
                f"wget -q {cloudflared_url} -O /usr/local/bin/cloudflared",
                "chmod +x /usr/local/bin/cloudflared"
            ]
        
        elif package_manager == 'zypper':
            return [
                "zypper refresh",
                "zypper install -y wget",
                f"wget -q {cloudflared_url} -O /usr/local/bin/cloudflared",
                "chmod +x /usr/local/bin/cloudflared"
            ]
        
        else:
            # Generic approach - download binary directly
            return [
                f"wget -q {cloudflared_url} -O /usr/local/bin/cloudflared",
                "chmod +x /usr/local/bin/cloudflared"
            ]
    
    def setup_tunnel_in_container(self, container_id: str, tunnel_token: str) -> bool:
        """Set up cloudflared tunnel service in a running container."""
        if not self.is_docker_available():
            return False
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("Setting up tunnel service...", total=None)
                
                # Install the tunnel service with the token
                result = subprocess.run(
                    ["docker", "exec", "--user", "root", container_id, "cloudflared", "service", "install", tunnel_token],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                progress.update(task, completed=1)
            
            if result.returncode == 0:
                self.console.print("[green]✓ Tunnel service installed successfully[/green]")
                return True
            else:
                self.console.print(f"[red]Error setting up tunnel service: {result.stderr}[/red]")
                return False
                
        except subprocess.TimeoutExpired:
            self.console.print("[red]Timeout setting up tunnel service[/red]")
            return False
        except Exception as e:
            self.console.print(f"[red]Error setting up tunnel service: {e}[/red]")
            return False
    
    def exec_command(self, container_id: str, command: str) -> Optional[str]:
        """Execute a command in a running container and return output."""
        if not self.is_docker_available():
            return None
        
        try:
            result = subprocess.run(
                ["docker", "exec", container_id, "bash", "-c", command],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                self.console.print(f"[red]Command failed: {result.stderr}[/red]")
                return None
                
        except Exception as e:
            self.console.print(f"[red]Error executing command: {e}[/red]")
            return None
    
    def get_container_logs(self, container_id: str, tail: int = 50) -> Optional[str]:
        """Get recent logs from a container."""
        if not self.is_docker_available():
            return None
        
        try:
            result = subprocess.run(
                ["docker", "logs", "--tail", str(tail), container_id],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return result.stdout + result.stderr
            else:
                return None
                
        except Exception as e:
            self.console.print(f"[red]Error getting container logs: {e}[/red]")
            return None
    
    def is_container_running(self, container_id: str) -> bool:
        """Check if a container is currently running."""
        if not self.is_docker_available():
            return False
        
        try:
            result = subprocess.run(
                ["docker", "ps", "-q", "--filter", f"id={container_id}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return result.returncode == 0 and result.stdout.strip() != ""
            
        except Exception as e:
            self.console.print(f"[red]Error checking container status: {e}[/red]")
            return False
    
    def get_container_status(self, container_id: str) -> Optional[str]:
        """Get the status of a container."""
        if not self.is_docker_available():
            return None
        
        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--format", "{{.Status}}", "--filter", f"id={container_id}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return None
                
        except Exception as e:
            self.console.print(f"[red]Error getting container status: {e}[/red]")
            return None
    
    def ensure_jupyter_running(self, container_id: str, jupyter_port: int = 8888, jupyter_token: Optional[str] = None, force_restart: bool = False) -> tuple[bool, Optional[str]]:
        """Ensure Jupyter Lab is running in the container.
        
        Args:
            container_id: Docker container ID
            jupyter_port: Port for Jupyter to listen on
            jupyter_token: Token to use for Jupyter authentication
            force_restart: If True, skip the "already running" check and start Jupyter with our token
        
        Returns:
            tuple: (success, jupyter_token) where success is bool and jupyter_token is the token used
        """
        if not self.is_docker_available():
            return False, None
        
        # Use provided token or generate one
        if not jupyter_token:
            jupyter_token = self.generate_jupyter_token()
        
        try:
            # Check if Jupyter is already running (unless we want to force restart)
            if not force_restart and self._is_jupyter_running(container_id, jupyter_port):
                self.console.print("[yellow]⚠ Jupyter is already running with unknown token[/yellow]")
                self.console.print("[dim]Consider using --force to restart with your token[/dim]")
                return True, jupyter_token
            
            # Try to start Jupyter Lab
            self.console.print("[yellow]Starting Jupyter Lab with custom token...[/yellow]")
            
            # Improved Jupyter startup commands with better compatibility
            jupyter_commands = [
                # Jupyter Lab (modern preferred)
                f"jupyter lab --ip=0.0.0.0 --port={jupyter_port} --no-browser --allow-root --ServerApp.token={jupyter_token} --ServerApp.allow_origin='*' --ServerApp.base_url=/ --ServerApp.terminado_settings='{{\"shell_command\":[\"/bin/bash\"]}}'",
                # Jupyter Lab with python -m (fallback)
                f"python -m jupyter lab --ip=0.0.0.0 --port={jupyter_port} --no-browser --allow-root --ServerApp.token={jupyter_token} --ServerApp.allow_origin='*'",
                # Jupyter Notebook (legacy compatibility)
                f"jupyter notebook --ip=0.0.0.0 --port={jupyter_port} --no-browser --allow-root --NotebookApp.token={jupyter_token} --NotebookApp.allow_origin='*'",
                # Jupyter Notebook with python -m
                f"python -m jupyter notebook --ip=0.0.0.0 --port={jupyter_port} --no-browser --allow-root --NotebookApp.token={jupyter_token} --NotebookApp.allow_origin='*'"
            ]
            
            for i, cmd in enumerate(jupyter_commands):
                try:
                    # Start Jupyter in background
                    result = subprocess.run(
                        ["docker", "exec", "-d", container_id, "bash", "-c", cmd],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.returncode == 0:
                        # Wait a moment and check if it's running
                        import time
                        time.sleep(5)  # Increased wait time for Jupyter to start
                        if self._is_jupyter_running(container_id, jupyter_port):
                            self.console.print("[green]✓ Jupyter Lab started successfully[/green]")
                            return True, jupyter_token
                        elif i == 0:  # Only show this message on first attempt
                            self.console.print("[yellow]Trying alternative startup command...[/yellow]")
                        
                except subprocess.TimeoutExpired:
                    continue
                except Exception:
                    continue
            
            self.console.print("[yellow]⚠ Could not start Jupyter automatically[/yellow]")
            self.console.print("[dim]Tip: Ensure Jupyter is installed in your container[/dim]")
            return False, None
            
        except Exception as e:
            self.console.print(f"[red]Error ensuring Jupyter is running: {e}[/red]")
            return False, None
    
    def _is_jupyter_running(self, container_id: str, port: int) -> bool:
        """Check if Jupyter is running on the specified port."""
        try:
            # Check if the port is listening
            result = subprocess.run(
                ["docker", "exec", container_id, "netstat", "-tln"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return f":{port}" in result.stdout
            
            # Fallback: check for Jupyter processes
            result = subprocess.run(
                ["docker", "exec", container_id, "pgrep", "-f", "jupyter"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            return result.returncode == 0
            
        except Exception:
            return False
    
    def get_jupyter_startup_command(self, jupyter_port: int = 8888, jupyter_token: Optional[str] = None) -> str:
        """Get a universal Jupyter startup command."""
        if not jupyter_token:
            jupyter_token = self.generate_jupyter_token()
            
        return (
            f"jupyter lab --ip=0.0.0.0 --port={jupyter_port} "
            f"--no-browser --allow-root --token={jupyter_token} "
            f"--NotebookApp.allow_origin='*' "
            f"--ServerApp.terminado_settings='{{\"shell_command\":[\"/bin/bash\"]}}'"
        )
    
    def generate_jupyter_token(self) -> str:
        """Generate a secure Jupyter token."""
        import secrets
        return secrets.token_hex(32)  # 64-character hex token

    def uninstall_cloudflared_service(self, container_id: str) -> bool:
        """Uninstall cloudflared service from a running container."""
        if not self.is_docker_available():
            return False
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("Uninstalling cloudflared service...", total=None)
                
                # Uninstall the cloudflared service
                result = subprocess.run(
                    ["docker", "exec", "--user", "root", container_id, "cloudflared", "service", "uninstall"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                progress.update(task, completed=1)
            
            if result.returncode == 0:
                self.console.print("[green]✓ Cloudflared service uninstalled successfully[/green]")
                return True
            else:
                # Don't treat this as a hard error since the service might not be installed
                self.console.print(f"[yellow]Warning: Could not uninstall cloudflared service: {result.stderr}[/yellow]")
                return True
                
        except subprocess.TimeoutExpired:
            self.console.print("[yellow]Warning: Timeout uninstalling cloudflared service[/yellow]")
            return True
        except Exception as e:
            self.console.print(f"[yellow]Warning: Error uninstalling cloudflared service: {e}[/yellow]")
            return True

    def stop_and_remove_container(self, container_id: str, force: bool = False) -> bool:
        """Stop and remove a container."""
        if not self.is_docker_available():
            return False
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("Stopping and removing container...", total=2)
                
                # Stop the container
                stop_result = self.stop_container(container_id)
                progress.update(task, advance=1)
                
                # Remove the container
                remove_result = self.remove_container(container_id, force=force)
                progress.update(task, advance=1)
                
                if stop_result and remove_result:
                    self.console.print(f"[green]✓ Container {container_id[:12]} stopped and removed[/green]")
                    return True
                else:
                    self.console.print(f"[yellow]Warning: Issues stopping/removing container {container_id[:12]}[/yellow]")
                    return False
                    
        except Exception as e:
            self.console.print(f"[red]Error stopping/removing container: {e}[/red]")
            return False

    def cleanup_container_and_tunnel(
        self, 
        container_id: str, 
        tunnel_id: Optional[str] = None,
        project_id: Optional[str] = None,
        force: bool = False
    ) -> bool:
        """Comprehensive cleanup of container, tunnel service, and optionally tunnel/project."""
        if not self.is_docker_available():
            return False
            
        success = True
        
        try:
            # Check if container is running
            if self.is_container_running(container_id):
                # Step 1: Uninstall cloudflared service if container is running
                self.console.print("[yellow]Cleaning up cloudflared service...[/yellow]")
                if not self.uninstall_cloudflared_service(container_id):
                    success = False
                
                # Give it a moment for the service to stop
                import time
                time.sleep(2)
            
            # Step 2: Stop and remove container
            self.console.print("[yellow]Stopping and removing container...[/yellow]")
            if not self.stop_and_remove_container(container_id, force=force):
                success = False
            
            if success:
                self.console.print("[green]✓ Container cleanup completed successfully[/green]")
            else:
                self.console.print("[yellow]⚠ Container cleanup completed with warnings[/yellow]")
            
            return success
            
        except Exception as e:
            self.console.print(f"[red]Error during container cleanup: {e}[/red]")
            return False


class MockContainer:
    """Mock container object to simulate Docker container."""
    
    def __init__(self, container_id: str):
        """Initialize mock container."""
        self.id = container_id
        self.short_id = container_id[:12] if len(container_id) > 12 else container_id 