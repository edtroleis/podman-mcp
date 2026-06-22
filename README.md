# podman-mcp

[![PyPI version](https://img.shields.io/pypi/v/podman-mcp)](https://pypi.org/project/podman-mcp)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Podman](https://img.shields.io/badge/Podman-892CA0?logo=podman&logoColor=white)](https://podman.io)
[![Claude](https://img.shields.io/badge/Claude-D97706?logo=anthropic&logoColor=white)](https://claude.ai)
[![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-000000?logo=github&logoColor=white)](https://github.com/features/copilot)
[![ChatGPT](https://img.shields.io/badge/ChatGPT-74aa9c?logo=openai&logoColor=white)](https://chatgpt.com)
[![Cursor](https://img.shields.io/badge/Cursor-000000?logo=cursor&logoColor=white)](https://www.cursor.com)
[![Windsurf](https://img.shields.io/badge/Windsurf-0098FF?logo=codeium&logoColor=white)](https://windsurf.com)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that exposes [Podman](https://podman.io) container management as tools for AI assistants such as [Claude](https://claude.ai), [GitHub Copilot](https://github.com/features/copilot), [ChatGPT](https://chatgpt.com), [Cursor](https://www.cursor.com) and [Windsurf](https://windsurf.com).

With `podman-mcp` you can manage containers and images through natural language — no need to remember CLI flags.

> "Show me all running containers"  
> "Pull the nginx image and run it on port 8080"  
> "Show me the last 100 log lines from myapp"

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Client Configuration](#client-configuration)
- [Using from the Terminal](#using-from-the-terminal)
- [Available Tools](#available-tools)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Adding New Tools](#adding-new-tools)
- [Releasing a New Version](#releasing-a-new-version)
- [Contributing](#contributing)
- [License](#license)

---

## Requirements

- Python 3.10+
- [Podman](https://podman.io/docs/installation) installed and available in `$PATH`
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI, [GitHub Copilot](https://github.com/features/copilot), [Cursor](https://www.cursor.com), [Windsurf](https://windsurf.com), [ChatGPT](https://chatgpt.com) or any MCP-compatible client

---

## Installation

### Using pip (recommended)

```bash
pip install podman-mcp
```

### From source

```bash
git clone https://github.com/edtroleis/podman-mcp.git
cd podman-mcp

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Client Configuration

### Claude Code

**Via pip:**

```bash
claude mcp add --scope user podman-mcp -- podman-mcp
```

**From source:**

```bash
claude mcp add --scope user podman-mcp -- /absolute/path/to/podman-mcp/.venv/bin/podman-mcp
```

The `--scope user` flag makes the server available across all projects.

Verify:

```bash
claude mcp list
```

#### Skip confirmation prompts

By default, Claude asks for confirmation before calling each tool. To allow all podman-mcp tools to run without prompts, add the following to `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "mcp__podman-mcp__*"
    ]
  }
}
```

---

### GitHub Copilot (VS Code)

Create or edit `.vscode/mcp.json` in your workspace.

**Via pip:**

```json
{
  "servers": {
    "podman-mcp": {
      "type": "stdio",
      "command": "podman-mcp"
    }
  }
}
```

**From source:**

```json
{
  "servers": {
    "podman-mcp": {
      "type": "stdio",
      "command": "/absolute/path/to/podman-mcp/.venv/bin/podman-mcp"
    }
  }
}
```

Requires VS Code 1.99+ with GitHub Copilot agent mode enabled.

> **Note:** VS Code does not auto-start MCP servers. After opening Copilot Chat, click the **Start** button next to `podman-mcp` in the Tools section once per VS Code session. This is a VS Code security design decision and cannot be configured away.

---

### Cursor

Create or edit `~/.cursor/mcp.json`.

**Via pip:**

```json
{
  "mcpServers": {
    "podman-mcp": {
      "command": "podman-mcp"
    }
  }
}
```

**From source:**

```json
{
  "mcpServers": {
    "podman-mcp": {
      "command": "/absolute/path/to/podman-mcp/.venv/bin/podman-mcp"
    }
  }
}
```

---

### Windsurf

Create or edit `~/.codeium/windsurf/mcp_config.json`.

**Via pip:**

```json
{
  "mcpServers": {
    "podman-mcp": {
      "command": "podman-mcp"
    }
  }
}
```

**From source:**

```json
{
  "mcpServers": {
    "podman-mcp": {
      "command": "/absolute/path/to/podman-mcp/.venv/bin/podman-mcp"
    }
  }
}
```

---

### ChatGPT and other HTTP clients

Start the server in SSE mode:

**Via pip:**

```bash
podman-mcp --transport sse --host 127.0.0.1 --port 8000
```

**From source:**

```bash
/absolute/path/to/podman-mcp/.venv/bin/podman-mcp --transport sse --host 127.0.0.1 --port 8000
```

The MCP endpoint will be available at:

```
http://127.0.0.1:8000/sse
```

Configure your client to connect to that URL as a remote MCP server.

---

## Using from the Terminal

You can interact with podman-mcp directly from the terminal using the Claude Code CLI — no IDE required.

### Claude Code CLI

Once podman-mcp is registered with `--scope user`, start an interactive session:

```bash
claude
```

Then ask naturally:

```
How many images do I have locally?
Pull nginx:latest
Show logs from my api container
List all running containers
Remove the alpine image
```

### Other AI CLIs (HTTP mode)

For AI tools that support remote MCP over HTTP, start the server in SSE mode first:

```bash
podman-mcp --transport sse --host 127.0.0.1 --port 8000
```

Then point your AI CLI client to `http://127.0.0.1:8000/sse`.

---

## Available Tools

### Images

| Tool | Description | Parameters |
|---|---|---|
| `list_images` | List all local images | — |
| `pull_image` | Pull an image from a registry | `image: str` |
| `remove_image` | Remove an image | `image: str`, `force: bool` |
| `build_image` | Build an image from a Dockerfile | `tag: str`, `dockerfile: str`, `context: str` |
| `tag_image` | Tag an image with a new name | `source: str`, `target: str` |
| `push_image` | Push an image to a registry | `image: str` |
| `image_history` | Show layer history of an image | `image: str` |
| `search_image` | Search for images in registries | `term: str` |
| `save_image` | Save an image to a tar archive | `image: str`, `output: str` |
| `load_image` | Load an image from a tar archive | `path: str` |
| `prune_images` | Remove unused images | `all: bool` |

### Containers

| Tool | Description | Parameters |
|---|---|---|
| `list_containers` | List containers | `all: bool` (include stopped) |
| `run_container` | Run a container | `image: str`, `args: str` |
| `start_container` | Start a stopped container | `name: str` |
| `stop_container` | Stop a running container | `name: str` |
| `restart_container` | Restart a container | `name: str` |
| `pause_container` | Pause all processes in a container | `name: str` |
| `unpause_container` | Resume a paused container | `name: str` |
| `rename_container` | Rename a container | `name: str`, `new_name: str` |
| `remove_container` | Remove a container | `name: str`, `force: bool` |
| `container_logs` | Fetch container logs | `name: str`, `tail: int` |
| `exec_in_container` | Run a command inside a container | `name: str`, `command: str` |
| `inspect_container` | Inspect container configuration | `name: str` |
| `container_stats` | Show resource usage for running containers | `name: str` (empty for all) |
| `container_top` | Show running processes inside a container | `name: str` |
| `container_port` | List port mappings of a container | `name: str` |
| `container_diff` | Show filesystem changes in a container | `name: str` |
| `copy_to_container` | Copy files between host and container | `src: str`, `dest: str` |

### Networks

| Tool | Description | Parameters |
|---|---|---|
| `network_list` | List all networks | — |
| `network_create` | Create a new network | `name: str` |
| `network_remove` | Remove a network | `name: str` |
| `network_inspect` | Inspect a network | `name: str` |
| `network_connect` | Connect a container to a network | `network: str`, `container: str` |
| `network_disconnect` | Disconnect a container from a network | `network: str`, `container: str` |
| `network_prune` | Remove all unused networks | — |

### Volumes

| Tool | Description | Parameters |
|---|---|---|
| `volume_list` | List all volumes | — |
| `volume_create` | Create a new volume | `name: str` |
| `volume_remove` | Remove a volume | `name: str` |
| `volume_inspect` | Inspect a volume | `name: str` |
| `volume_prune` | Remove all unused volumes | — |

### Pods

| Tool | Description | Parameters |
|---|---|---|
| `pod_list` | List pods | `all: bool` (include stopped) |
| `pod_create` | Create a new pod | `name: str` |
| `pod_remove` | Remove a pod | `name: str`, `force: bool` |
| `pod_start` | Start a pod and all its containers | `name: str` |
| `pod_stop` | Stop a pod and all its containers | `name: str` |
| `pod_restart` | Restart a pod and all its containers | `name: str` |
| `pod_inspect` | Inspect a pod | `name: str` |
| `pod_stats` | Show resource usage stats for pods | `name: str` (empty for all) |

### Secrets

| Tool | Description | Parameters |
|---|---|---|
| `secret_list` | List all secrets | — |
| `secret_create` | Create a secret from a literal value | `name: str`, `value: str` |
| `secret_remove` | Remove a secret | `name: str` |
| `secret_inspect` | Inspect a secret (value is never revealed) | `name: str` |

### Generate

| Tool | Description | Parameters |
|---|---|---|
| `generate_kube` | Generate Kubernetes YAML from a pod or container | `name: str` |
| `generate_systemd` | Generate a systemd unit file for a container or pod | `name: str` |

### System

| Tool | Description | Parameters |
|---|---|---|
| `system_info` | Podman disk usage and system stats | — |
| `system_prune` | Remove all unused resources | `all: bool` |
| `system_events` | Show recent Podman events | `since: str`, `until: str`, `filter: str` |
| `podman_version` | Show Podman version information | — |
| `podman_info` | Show detailed host and runtime information | — |
| `login_registry` | Login to a container registry | `registry: str`, `username: str`, `password: str` |

---

## Usage Examples

Once registered, interact with Podman using natural language. Examples by category:

### Images

```
How many images do I have locally?
```
```
Pull the python:3.12-slim image from Docker Hub
```
```
Build an image tagged myapp:latest from the Dockerfile in the current directory
```
```
Show the layer history of the debian:latest image
```
```
Tag myapp:latest as localhost:8082/myapp:1.0
```
```
Push localhost:8082/myapp:1.0 to the registry
```
```
Search for postgres images in Docker Hub
```
```
Save the myapp:latest image to /tmp/myapp.tar
```
```
Remove the alpine image
```

### Containers

```
List all running containers
```
```
Show me all containers, including stopped ones
```
```
Run nginx in detached mode, exposing port 8080 on the host
```
```
Start the stopped api container
```
```
Restart the db container
```
```
Show the last 200 log lines from the api container
```
```
What is the IP address of the db container?
```
```
Show CPU and memory usage for all running containers
```
```
Execute the command "df -h" inside the api container
```
```
Show all port mappings of the web container
```
```
Remove all stopped containers
```

### Networks

```
List all networks
```
```
Create a network called backend-net
```
```
Connect the api container to the backend-net network
```
```
Remove unused networks
```

### Volumes

```
List all volumes
```
```
Create a volume called postgres-data
```
```
Remove unused volumes
```

### Pods

```
List all pods, including stopped ones
```
```
Create a pod called my-pod
```
```
Start the my-pod pod
```
```
Stop the my-pod pod
```
```
Remove the my-pod pod and all its containers
```
```
Show resource usage for all pods
```

### Secrets

```
List all secrets
```
```
Create a secret called db-password with value s3cr3t
```
```
Show metadata for the db-password secret
```
```
Remove the db-password secret
```

### Generate

```
Generate Kubernetes YAML for the my-pod pod
```
```
Generate a systemd unit file for the api container
```

### System & Registry

```
Show Podman disk usage and system stats
```
```
Show detailed Podman host information
```
```
Show the Podman version
```
```
Show recent container start events from the last hour
```
```
Remove all unused containers, images, networks and volumes
```
```
Login to localhost:8082 with my credentials
```

---

## Project Structure

```
podman-mcp/
├── .github/
│   └── workflows/
│       └── publish.yml    # GitHub Actions — publishes to PyPI on tag push
├── podman_mcp/
│   ├── __init__.py
│   └── server.py          # MCP server — all tools are defined here
├── tests/
│   └── test_server.py     # pytest test suite
├── pyproject.toml         # Project metadata and build config
├── requirements.txt       # Runtime dependencies
├── CONTRIBUTING.md        # How to contribute
├── LICENSE                # MIT License
└── README.md
```

---

## Testing

Tests use [pytest](https://docs.pytest.org) and mock `subprocess.run` so no Podman installation is required to run them.

Install dev dependencies and run the suite:

```bash
pip install -e ".[dev]"
pytest tests/
```

Run with verbose output:

```bash
pytest tests/ -v
```

---

## Adding New Tools

Open [podman_mcp/server.py](podman_mcp/server.py) and add a new function decorated with `@mcp.tool()`:

```python
@mcp.tool()
def your_tool_name(param: str) -> str:
    """Clear description — the AI assistant uses this to decide when to call the tool."""
    return run(f"<podman subcommand> {param}")
```

No re-registration is needed. Restart your AI client session to pick up the new tool.

---

## Releasing a New Version

1. Bump the version in `pyproject.toml`:

```toml
[project]
version = "1.2.3"
```

2. Commit and push:

```bash
git add pyproject.toml
git commit -m "bump version to 1.2.3"
git push
```

3. Create and push a tag — this triggers the publish pipeline:

```bash
git tag v1.2.3
git push origin v1.2.3
```

The [GitHub Actions workflow](.github/workflows/publish.yml) will run tests, publish to PyPI and create a GitHub Release automatically.

> **Note:** PyPI does not allow re-uploading the same version. Always bump the version before tagging.

### Release Notes

Release notes are generated automatically from commits and PRs merged since the last tag, grouped by label:

| Label | Section |
|---|---|
| `enhancement`, `feature` | New Features |
| `bug`, `fix` | Bug Fixes |
| `documentation`, `docs` | Documentation |
| anything else | Other Changes |

No conventional commit format required — just label your PRs on GitHub before merging.

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

[MIT](LICENSE)
