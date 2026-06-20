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
