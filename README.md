# podman-mcp

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that exposes [Podman](https://podman.io) container management as tools for AI assistants such as [Claude](https://claude.ai), [GitHub Copilot](https://github.com/features/copilot), [ChatGPT](https://chatgpt.com), [Cursor](https://www.cursor.com) and [Windsurf](https://windsurf.com).

With `podman-mcp` you can manage containers and images through natural language — no need to remember CLI flags.

> "Show me all running containers"  
> "Pull the nginx image and run it on port 8080"  
> "Show me the last 100 log lines from myapp"

---

## Requirements

- Python 3.10+
- [Podman](https://podman.io/docs/installation) installed and available in `$PATH`
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI **or** any MCP-compatible client

---

## Installation

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

```bash
claude mcp add --scope user podman-mcp -- /absolute/path/to/podman-mcp/.venv/bin/python3 /absolute/path/to/podman-mcp/server.py
```

The `--scope user` flag makes the server available across all projects, not just the current directory.

Verify:

```bash
claude mcp list
```

---

### GitHub Copilot (VS Code)

Create `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "podman-mcp": {
      "type": "stdio",
      "command": "/absolute/path/to/podman-mcp/.venv/bin/python3",
      "args": ["/absolute/path/to/podman-mcp/server.py"]
    }
  }
}
```

Requires VS Code 1.99+ with GitHub Copilot agent mode enabled.

---

### Cursor

Create or edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "podman-mcp": {
      "command": "/absolute/path/to/podman-mcp/.venv/bin/python3",
      "args": ["/absolute/path/to/podman-mcp/server.py"]
    }
  }
}
```

---

### Windsurf

Create or edit `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "podman-mcp": {
      "command": "/absolute/path/to/podman-mcp/.venv/bin/python3",
      "args": ["/absolute/path/to/podman-mcp/server.py"]
    }
  }
}
```

---

### ChatGPT and other HTTP clients

Start the server in SSE mode:

```bash
python3 server.py --transport sse --host 127.0.0.1 --port 8000
```

The MCP endpoint will be available at:

```
http://127.0.0.1:8000/sse
```

Configure your client to connect to that URL as a remote MCP server.

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

Once registered, ask Claude naturally:

```
How many images do I have locally?
Show me all containers, including stopped ones.
Pull the alpine:latest image.
Run nginx on port 8080 in detached mode.
Show me the last 200 log lines from the api container.
What is the IP address of the db container?
Remove all stopped containers.
Build an image tagged myapp:latest from the Dockerfile in the current directory.
Tag myapp:latest as localhost:8082/myapp:1.0 and push it.
List all networks and volumes.
Create a pod called my-pod.
Show CPU and memory usage for all running containers.
Login to localhost:8082 with my credentials.
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
    """Clear description — Claude uses this to decide when to call the tool."""
    return run(f"<podman subcommand> {param}")
```

No re-registration is needed. Restart your Claude Code session to pick up the new tool.

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

[MIT](LICENSE)
