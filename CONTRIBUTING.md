# Contributing to podman-mcp

Thank you for your interest in contributing! This guide covers everything you need to get started.

---

## Ways to Contribute

- **New tools** — expose more Podman subcommands as MCP tools
- **Bug fixes** — fix incorrect behavior or error handling
- **Documentation** — improve examples, fix typos, add translations
- **Testing** — add test cases for existing or new tools

---

## Getting Started

### 1. Fork and clone

```bash
git clone https://github.com/<your-username>/podman-mcp.git
cd podman-mcp
```

### 2. Set up the environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Verify Podman is available

```bash
podman --version
```

---

## Adding a New Tool

All tools live in `server.py`. Adding one is straightforward:

```python
@mcp.tool()
def your_tool(param: str) -> str:
    """One-line description. Claude uses this to decide when to call the tool."""
    return run(f"<podman subcommand> {param}")
```

**Guidelines for tools:**

- One action per tool — keep the scope narrow
- Write a clear docstring — it is what Claude reads to select the tool
- Accept typed parameters — use `str`, `bool`, `int` (no `Any`)
- Return a `str` — raw Podman output is fine; add context if the output is not self-explanatory
- Handle the common failure modes — e.g. container not found, image not available

---

## Submitting a Pull Request

1. Create a branch from `main`:
   ```bash
   git checkout -b feat/my-new-tool
   ```

2. Make your changes in `server.py` (and update `README.md` if you added a tool).

3. Test manually:
   ```bash
   # Start the server and send a test request via stdin
   echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
     | .venv/bin/python3 server.py
   ```

4. Commit with a clear message:
   ```bash
   git commit -m "feat: add network_list tool"
   ```

5. Push and open a Pull Request against `main`.

---

## Pull Request Checklist

- [ ] Tool has a clear, one-line docstring
- [ ] Parameters are typed
- [ ] New tool is listed in the `README.md` tools table
- [ ] Manually tested against a live Podman installation

---

## Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Use for |
|---|---|
| `feat:` | New tool or feature |
| `fix:` | Bug fix |
| `docs:` | Documentation changes only |
| `refactor:` | Code change with no behavior change |
| `chore:` | Dependency updates, config changes |

---

## Reporting Issues

Open an issue and include:

- Your OS and Podman version (`podman --version`)
- Python version (`python3 --version`)
- The natural language prompt you used
- The error or unexpected output you received

---

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Keep functions small and focused
- No comments unless the intent is genuinely non-obvious
