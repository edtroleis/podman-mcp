import argparse
import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("podman-mcp")


def run(cmd: str) -> str:
    result = subprocess.run(
        f"podman {cmd}",
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout.strip() or result.stderr.strip()


@mcp.tool()
def list_images() -> str:
    """List all local Podman images."""
    return run("images")


@mcp.tool()
def list_containers(all: bool = False) -> str:
    """List containers. Set all=true to include stopped ones."""
    flag = "-a" if all else ""
    return run(f"ps {flag}")


@mcp.tool()
def pull_image(image: str) -> str:
    """Pull an image from a registry. Example: image='nginx:latest'"""
    return run(f"pull {image}")


@mcp.tool()
def stop_container(name: str) -> str:
    """Stop a running container by name or ID."""
    return run(f"stop {name}")


@mcp.tool()
def remove_container(name: str, force: bool = False) -> str:
    """Remove a container by name or ID."""
    flag = "-f" if force else ""
    return run(f"rm {flag} {name}")


@mcp.tool()
def remove_image(image: str, force: bool = False) -> str:
    """Remove an image by name or ID."""
    flag = "-f" if force else ""
    return run(f"rmi {flag} {image}")


@mcp.tool()
def container_logs(name: str, tail: int = 50) -> str:
    """Get logs from a container."""
    return run(f"logs --tail {tail} {name}")


@mcp.tool()
def run_container(image: str, args: str = "") -> str:
    """Run a container from an image. Extra args optional (e.g. '-d -p 8080:80')"""
    return run(f"run {args} {image}")


@mcp.tool()
def system_info() -> str:
    """Show Podman system info and disk usage."""
    return run("system df")


@mcp.tool()
def inspect_container(name: str) -> str:
    """Inspect a container and return its configuration details."""
    return run(f"inspect {name}")


@mcp.tool()
def exec_in_container(name: str, command: str) -> str:
    """Execute a command inside a running container."""
    return run(f"exec {name} {command}")


@mcp.tool()
def build_image(tag: str, dockerfile: str = "Dockerfile", context: str = ".") -> str:
    """Build an image from a Dockerfile. Example: tag='myapp:latest', dockerfile='./Dockerfile', context='.'"""
    return run(f"build --squash-all -t {tag} -f {dockerfile} {context}")


@mcp.tool()
def tag_image(source: str, target: str) -> str:
    """Tag an image with a new name. Example: source='myapp:latest', target='registry/myapp:1.0'"""
    return run(f"tag {source} {target}")


@mcp.tool()
def push_image(image: str) -> str:
    """Push an image to a registry. Example: image='registry/myapp:1.0'"""
    return run(f"push {image}")


@mcp.tool()
def image_history(image: str) -> str:
    """Show layer history of an image."""
    return run(f"history {image}")


@mcp.tool()
def container_stats(name: str = "") -> str:
    """Show resource usage stats for running containers. Leave name empty for all."""
    flag = "--no-stream"
    target = name if name else "--all"
    return run(f"stats {flag} {target}")


@mcp.tool()
def network_list() -> str:
    """List all Podman networks."""
    return run("network ls")


@mcp.tool()
def network_create(name: str) -> str:
    """Create a new Podman network."""
    return run(f"network create {name}")


@mcp.tool()
def network_remove(name: str) -> str:
    """Remove a Podman network by name."""
    return run(f"network rm {name}")


@mcp.tool()
def volume_list() -> str:
    """List all Podman volumes."""
    return run("volume ls")


@mcp.tool()
def volume_create(name: str) -> str:
    """Create a new Podman volume."""
    return run(f"volume create {name}")


@mcp.tool()
def volume_remove(name: str) -> str:
    """Remove a Podman volume by name."""
    return run(f"volume rm {name}")


@mcp.tool()
def pod_list(all: bool = False) -> str:
    """List pods. Set all=true to include stopped ones."""
    flag = "--all" if all else ""
    return run(f"pod list {flag}")


@mcp.tool()
def pod_create(name: str) -> str:
    """Create a new pod."""
    return run(f"pod create --name {name}")


@mcp.tool()
def pod_remove(name: str, force: bool = False) -> str:
    """Remove a pod by name or ID."""
    flag = "-f" if force else ""
    return run(f"pod rm {flag} {name}")


@mcp.tool()
def login_registry(registry: str, username: str, password: str) -> str:
    """Login to a container registry."""
    return run(f"login {registry} -u {username} -p {password}")


# Containers

@mcp.tool()
def start_container(name: str) -> str:
    """Start a stopped container by name or ID."""
    return run(f"start {name}")


@mcp.tool()
def restart_container(name: str) -> str:
    """Restart a running or stopped container by name or ID."""
    return run(f"restart {name}")


@mcp.tool()
def pause_container(name: str) -> str:
    """Pause all processes in a running container."""
    return run(f"pause {name}")


@mcp.tool()
def unpause_container(name: str) -> str:
    """Resume a paused container."""
    return run(f"unpause {name}")


@mcp.tool()
def rename_container(name: str, new_name: str) -> str:
    """Rename a container."""
    return run(f"rename {name} {new_name}")


@mcp.tool()
def copy_to_container(src: str, dest: str) -> str:
    """Copy files between host and container. Use 'container:path' format for the container side. Example: src='./file.txt', dest='mycontainer:/tmp/file.txt'"""
    return run(f"cp {src} {dest}")


@mcp.tool()
def container_top(name: str) -> str:
    """Show running processes inside a container."""
    return run(f"top {name}")


@mcp.tool()
def container_port(name: str) -> str:
    """List port mappings of a container."""
    return run(f"port {name}")


@mcp.tool()
def container_diff(name: str) -> str:
    """Show filesystem changes made inside a container since it was started."""
    return run(f"diff {name}")


# Images

@mcp.tool()
def search_image(term: str) -> str:
    """Search for images in registries. Example: term='nginx'"""
    return run(f"search {term}")


@mcp.tool()
def save_image(image: str, output: str) -> str:
    """Save an image to a tar archive. Example: image='myapp:latest', output='/tmp/myapp.tar'"""
    return run(f"save -o {output} {image}")


@mcp.tool()
def load_image(path: str) -> str:
    """Load an image from a tar archive. Example: path='/tmp/myapp.tar'"""
    return run(f"load -i {path}")


@mcp.tool()
def prune_images(all: bool = False) -> str:
    """Remove unused images. Set all=true to also remove images not referenced by any container."""
    flag = "-a" if all else ""
    return run(f"image prune -f {flag}")


# Networks

@mcp.tool()
def network_inspect(name: str) -> str:
    """Inspect a network and return its configuration."""
    return run(f"network inspect {name}")


@mcp.tool()
def network_connect(network: str, container: str) -> str:
    """Connect a container to a network."""
    return run(f"network connect {network} {container}")


@mcp.tool()
def network_disconnect(network: str, container: str) -> str:
    """Disconnect a container from a network."""
    return run(f"network disconnect {network} {container}")


@mcp.tool()
def network_prune() -> str:
    """Remove all unused networks."""
    return run("network prune -f")


# Volumes

@mcp.tool()
def volume_inspect(name: str) -> str:
    """Inspect a volume and return its configuration."""
    return run(f"volume inspect {name}")


@mcp.tool()
def volume_prune() -> str:
    """Remove all unused volumes."""
    return run("volume prune -f")


# Pods

@mcp.tool()
def pod_start(name: str) -> str:
    """Start a pod and all its containers."""
    return run(f"pod start {name}")


@mcp.tool()
def pod_stop(name: str) -> str:
    """Stop a pod and all its containers."""
    return run(f"pod stop {name}")


@mcp.tool()
def pod_restart(name: str) -> str:
    """Restart a pod and all its containers."""
    return run(f"pod restart {name}")


@mcp.tool()
def pod_inspect(name: str) -> str:
    """Inspect a pod and return its configuration details."""
    return run(f"pod inspect {name}")


@mcp.tool()
def pod_stats(name: str = "") -> str:
    """Show resource usage stats for pods. Leave name empty for all pods."""
    target = name if name else "--all"
    return run(f"pod stats --no-stream {target}")


# System

@mcp.tool()
def system_prune(all: bool = False) -> str:
    """Remove all unused containers, images, networks and volumes. Set all=true to also remove unused images."""
    flag = "-a" if all else ""
    return run(f"system prune -f {flag}")


@mcp.tool()
def podman_version() -> str:
    """Show Podman version information."""
    return run("version")


@mcp.tool()
def podman_info() -> str:
    """Show detailed Podman host and runtime information."""
    return run("info")


@mcp.tool()
def system_events(since: str = "", until: str = "", filter: str = "") -> str:
    """Show recent Podman events. Example: since='1h', filter='event=start'"""
    args = "--stream=false"
    if since:
        args += f" --since {since}"
    if until:
        args += f" --until {until}"
    if filter:
        args += f" --filter {filter}"
    return run(f"events {args}")


# Secrets

@mcp.tool()
def secret_list() -> str:
    """List all Podman secrets."""
    return run("secret ls")


@mcp.tool()
def secret_create(name: str, value: str) -> str:
    """Create a secret from a literal value. Example: name='db-password', value='s3cr3t'"""
    return run(f"secret create {name} - <<< '{value}'")


@mcp.tool()
def secret_remove(name: str) -> str:
    """Remove a secret by name or ID."""
    return run(f"secret rm {name}")


@mcp.tool()
def secret_inspect(name: str) -> str:
    """Inspect a secret and return its metadata (value is never revealed)."""
    return run(f"secret inspect {name}")


# Generate

@mcp.tool()
def generate_kube(name: str) -> str:
    """Generate Kubernetes YAML from a pod or container. Example: name='mypod'"""
    return run(f"generate kube {name}")


@mcp.tool()
def generate_systemd(name: str) -> str:
    """Generate systemd unit file for a container or pod. Example: name='mycontainer'"""
    return run(f"generate systemd --new {name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")
