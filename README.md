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
# 1. Clone the repository
git clone https://github.com/edtroleis/podman-mcp.git
cd podman-mcp

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Client Configuration

### Claude Code

If installed via pip:

```bash
claude mcp add --scope user podman-mcp -- podman-mcp
```

If installed from source:

```bash
claude mcp add --scope user podman-mcp -- /absolute/path/to/podman-mcp/.venv/bin/podman-mcp
```

The `--scope user` flag makes the server available across all projects, not just the current directory.

Verify:

```bash
claude mcp list
```

#### Skip confirmation prompts (user scope)

By default, Claude asks for confirmation before calling each tool. To allow all podman-mcp tools to run without prompts across all projects, add the following to `~/.claude/settings.json`:

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

Create `.vscode/mcp.json` in your workspace.

If installed via pip:

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

If installed from source:

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

If installed via pip:

```json
{
  "mcpServers": {
    "podman-mcp": {
      "command": "podman-mcp"
    }
  }
}
```

If installed from source:

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

If installed via pip:

```json
{
  "mcpServers": {
    "podman-mcp": {
      "command": "podman-mcp"
    }
  }
}
```

If installed from source:

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

Start the server in SSE mode.

If installed via pip:

```bash
podman-mcp --transport sse --host 127.0.0.1 --port 8000
```

If installed from source:

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

You can interact with podman-mcp directly from your Linux console using the Claude Code CLI — no IDE required.

### Claude Code CLI

Once podman-mcp is registered with `--scope user`, start an interactive session:

```bash
claude
```

Then ask naturally:

```
How many images do I have locally?
```
```
Pull nginx:latest
```
```
Show logs from my nexus container
```
```
List all running containers
```
```
Remove the alpine image
```

Claude will automatically use the podman-mcp tools to answer.

### Other AI CLIs (HTTP mode)

For AI tools that support remote MCP over HTTP, start the server in SSE mode first:

```bash
python3 /absolute/path/to/podman-mcp/server.py --transport sse --host 127.0.0.1 --port 8000
```

Then point your AI CLI client to:

```
http://127.0.0.1:8000/sse
```

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

### Containers

| Tool | Description | Parameters |
|---|---|---|
| `list_containers` | List containers | `all: bool` (include stopped) |
| `run_container` | Run a container | `image: str`, `args: str` |
| `stop_container` | Stop a running container | `name: str` |
| `remove_container` | Remove a container | `name: str`, `force: bool` |
| `container_logs` | Fetch container logs | `name: str`, `tail: int` |
| `exec_in_container` | Run a command inside a container | `name: str`, `command: str` |
| `inspect_container` | Inspect container configuration | `name: str` |
| `container_stats` | Show resource usage for running containers | `name: str` (empty for all) |

### Networks

| Tool | Description | Parameters |
|---|---|---|
| `network_list` | List all networks | — |
| `network_create` | Create a new network | `name: str` |
| `network_remove` | Remove a network | `name: str` |

### Volumes

| Tool | Description | Parameters |
|---|---|---|
| `volume_list` | List all volumes | — |
| `volume_create` | Create a new volume | `name: str` |
| `volume_remove` | Remove a volume | `name: str` |

### Pods

| Tool | Description | Parameters |
|---|---|---|
| `pod_list` | List pods | `all: bool` (include stopped) |
| `pod_create` | Create a new pod | `name: str` |
| `pod_remove` | Remove a pod | `name: str`, `force: bool` |

### System

| Tool | Description | Parameters |
|---|---|---|
| `system_info` | Podman disk usage and system stats | — |
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
Remove all stopped containers
```

### Networks & Volumes

```
List all networks
```
```
Create a network called backend-net
```
```
List all volumes
```
```
Create a volume called postgres-data
```
```
Remove the volume named postgres-data
```

### Pods

```
List all pods, including stopped ones
```
```
Create a pod called my-pod
```
```
Remove the pod my-pod and all its containers
```

### System & Registry

```
Show Podman disk usage and system stats
```
```
Login to localhost:8082 with my credentials
```

---

## Project Structure

```
podman-mcp/
├── server.py          # MCP server — all tools are defined here
├── requirements.txt   # Python dependencies
├── CONTRIBUTING.md    # How to contribute
├── LICENSE            # MIT License
└── README.md
```

---

## Adding New Tools

Open [server.py](server.py) and add a new function decorated with `@mcp.tool()`:

```python
@mcp.tool()
def your_tool_name(param: str) -> str:
    """Clear description — the AI assistant uses this to decide when to call the tool."""
    return run(f"<podman subcommand> {param}")
```

No re-registration is needed. Restart your AI client session to pick up the new tool.

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

[MIT](LICENSE)
