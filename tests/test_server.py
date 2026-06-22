from unittest.mock import patch, MagicMock
import pytest
import podman_mcp.server as server


def mock_subprocess(stdout="ok", stderr=""):
    m = MagicMock()
    m.stdout = stdout
    m.stderr = stderr
    return m


def cmd(mock_sub):
    """Return the shell command string passed to subprocess.run."""
    return mock_sub.call_args[0][0]


# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------

@patch("podman_mcp.server.subprocess.run")
def test_list_images(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.list_images()
    assert cmd(mock_sub) == "podman images"


@patch("podman_mcp.server.subprocess.run")
def test_pull_image(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.pull_image("nginx:latest")
    assert cmd(mock_sub) == "podman pull nginx:latest"


@patch("podman_mcp.server.subprocess.run")
def test_remove_image(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.remove_image("nginx:latest")
    assert "rmi" in cmd(mock_sub)
    assert "nginx:latest" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_remove_image_force(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.remove_image("nginx:latest", force=True)
    assert "-f" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_build_image(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.build_image("myapp:latest", "Dockerfile", ".")
    assert "build" in cmd(mock_sub)
    assert "-t myapp:latest" in cmd(mock_sub)
    assert "-f Dockerfile" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_tag_image(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.tag_image("myapp:latest", "registry/myapp:1.0")
    assert cmd(mock_sub) == "podman tag myapp:latest registry/myapp:1.0"


@patch("podman_mcp.server.subprocess.run")
def test_push_image(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.push_image("registry/myapp:1.0")
    assert cmd(mock_sub) == "podman push registry/myapp:1.0"


@patch("podman_mcp.server.subprocess.run")
def test_image_history(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.image_history("nginx:latest")
    assert cmd(mock_sub) == "podman history nginx:latest"


@patch("podman_mcp.server.subprocess.run")
def test_search_image(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.search_image("nginx")
    assert cmd(mock_sub) == "podman search nginx"


@patch("podman_mcp.server.subprocess.run")
def test_save_image(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.save_image("myapp:latest", "/tmp/myapp.tar")
    assert "save" in cmd(mock_sub)
    assert "-o /tmp/myapp.tar" in cmd(mock_sub)
    assert "myapp:latest" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_load_image(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.load_image("/tmp/myapp.tar")
    assert cmd(mock_sub) == "podman load -i /tmp/myapp.tar"


@patch("podman_mcp.server.subprocess.run")
def test_prune_images(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.prune_images()
    assert "image prune -f" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_prune_images_all(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.prune_images(all=True)
    assert "-a" in cmd(mock_sub)


# ---------------------------------------------------------------------------
# Containers
# ---------------------------------------------------------------------------

@patch("podman_mcp.server.subprocess.run")
def test_list_containers(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.list_containers()
    assert "ps" in cmd(mock_sub)
    assert "-a" not in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_list_containers_all(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.list_containers(all=True)
    assert "-a" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_run_container(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.run_container("nginx:latest", "-d -p 8080:80")
    assert "run" in cmd(mock_sub)
    assert "nginx:latest" in cmd(mock_sub)
    assert "-d -p 8080:80" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_start_container(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.start_container("mycontainer")
    assert cmd(mock_sub) == "podman start mycontainer"


@patch("podman_mcp.server.subprocess.run")
def test_stop_container(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.stop_container("mycontainer")
    assert cmd(mock_sub) == "podman stop mycontainer"


@patch("podman_mcp.server.subprocess.run")
def test_restart_container(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.restart_container("mycontainer")
    assert cmd(mock_sub) == "podman restart mycontainer"


@patch("podman_mcp.server.subprocess.run")
def test_pause_container(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.pause_container("mycontainer")
    assert cmd(mock_sub) == "podman pause mycontainer"


@patch("podman_mcp.server.subprocess.run")
def test_unpause_container(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.unpause_container("mycontainer")
    assert cmd(mock_sub) == "podman unpause mycontainer"


@patch("podman_mcp.server.subprocess.run")
def test_rename_container(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.rename_container("old", "new")
    assert cmd(mock_sub) == "podman rename old new"


@patch("podman_mcp.server.subprocess.run")
def test_remove_container(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.remove_container("mycontainer")
    assert "rm" in cmd(mock_sub)
    assert "mycontainer" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_remove_container_force(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.remove_container("mycontainer", force=True)
    assert "-f" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_container_logs(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.container_logs("mycontainer", tail=100)
    assert "logs" in cmd(mock_sub)
    assert "--tail 100" in cmd(mock_sub)
    assert "mycontainer" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_exec_in_container(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.exec_in_container("mycontainer", "df -h")
    assert cmd(mock_sub) == "podman exec mycontainer df -h"


@patch("podman_mcp.server.subprocess.run")
def test_inspect_container(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.inspect_container("mycontainer")
    assert cmd(mock_sub) == "podman inspect mycontainer"


@patch("podman_mcp.server.subprocess.run")
def test_container_stats_all(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.container_stats()
    assert "--all" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_container_stats_named(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.container_stats("mycontainer")
    assert "mycontainer" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_container_top(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.container_top("mycontainer")
    assert cmd(mock_sub) == "podman top mycontainer"


@patch("podman_mcp.server.subprocess.run")
def test_container_port(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.container_port("mycontainer")
    assert cmd(mock_sub) == "podman port mycontainer"


@patch("podman_mcp.server.subprocess.run")
def test_container_diff(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.container_diff("mycontainer")
    assert cmd(mock_sub) == "podman diff mycontainer"


@patch("podman_mcp.server.subprocess.run")
def test_copy_to_container(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.copy_to_container("./file.txt", "mycontainer:/tmp/file.txt")
    assert "cp" in cmd(mock_sub)
    assert "./file.txt" in cmd(mock_sub)
    assert "mycontainer:/tmp/file.txt" in cmd(mock_sub)


# ---------------------------------------------------------------------------
# Networks
# ---------------------------------------------------------------------------

@patch("podman_mcp.server.subprocess.run")
def test_network_list(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.network_list()
    assert cmd(mock_sub) == "podman network ls"


@patch("podman_mcp.server.subprocess.run")
def test_network_create(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.network_create("mynet")
    assert cmd(mock_sub) == "podman network create mynet"


@patch("podman_mcp.server.subprocess.run")
def test_network_remove(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.network_remove("mynet")
    assert cmd(mock_sub) == "podman network rm mynet"


@patch("podman_mcp.server.subprocess.run")
def test_network_inspect(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.network_inspect("mynet")
    assert cmd(mock_sub) == "podman network inspect mynet"


@patch("podman_mcp.server.subprocess.run")
def test_network_connect(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.network_connect("mynet", "mycontainer")
    assert cmd(mock_sub) == "podman network connect mynet mycontainer"


@patch("podman_mcp.server.subprocess.run")
def test_network_disconnect(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.network_disconnect("mynet", "mycontainer")
    assert cmd(mock_sub) == "podman network disconnect mynet mycontainer"


@patch("podman_mcp.server.subprocess.run")
def test_network_prune(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.network_prune()
    assert cmd(mock_sub) == "podman network prune -f"


# ---------------------------------------------------------------------------
# Volumes
# ---------------------------------------------------------------------------

@patch("podman_mcp.server.subprocess.run")
def test_volume_list(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.volume_list()
    assert cmd(mock_sub) == "podman volume ls"


@patch("podman_mcp.server.subprocess.run")
def test_volume_create(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.volume_create("myvol")
    assert cmd(mock_sub) == "podman volume create myvol"


@patch("podman_mcp.server.subprocess.run")
def test_volume_remove(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.volume_remove("myvol")
    assert cmd(mock_sub) == "podman volume rm myvol"


@patch("podman_mcp.server.subprocess.run")
def test_volume_inspect(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.volume_inspect("myvol")
    assert cmd(mock_sub) == "podman volume inspect myvol"


@patch("podman_mcp.server.subprocess.run")
def test_volume_prune(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.volume_prune()
    assert cmd(mock_sub) == "podman volume prune -f"


# ---------------------------------------------------------------------------
# Pods
# ---------------------------------------------------------------------------

@patch("podman_mcp.server.subprocess.run")
def test_pod_list(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.pod_list()
    assert "pod list" in cmd(mock_sub)
    assert "--all" not in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_pod_list_all(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.pod_list(all=True)
    assert "--all" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_pod_create(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.pod_create("mypod")
    assert cmd(mock_sub) == "podman pod create --name mypod"


@patch("podman_mcp.server.subprocess.run")
def test_pod_remove(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.pod_remove("mypod")
    assert "pod rm" in cmd(mock_sub)
    assert "mypod" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_pod_remove_force(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.pod_remove("mypod", force=True)
    assert "-f" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_pod_start(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.pod_start("mypod")
    assert cmd(mock_sub) == "podman pod start mypod"


@patch("podman_mcp.server.subprocess.run")
def test_pod_stop(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.pod_stop("mypod")
    assert cmd(mock_sub) == "podman pod stop mypod"


@patch("podman_mcp.server.subprocess.run")
def test_pod_restart(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.pod_restart("mypod")
    assert cmd(mock_sub) == "podman pod restart mypod"


@patch("podman_mcp.server.subprocess.run")
def test_pod_inspect(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.pod_inspect("mypod")
    assert cmd(mock_sub) == "podman pod inspect mypod"


@patch("podman_mcp.server.subprocess.run")
def test_pod_stats_all(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.pod_stats()
    assert "--all" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_pod_stats_named(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.pod_stats("mypod")
    assert "mypod" in cmd(mock_sub)


# ---------------------------------------------------------------------------
# Secrets
# ---------------------------------------------------------------------------

@patch("podman_mcp.server.subprocess.run")
def test_secret_list(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.secret_list()
    assert cmd(mock_sub) == "podman secret ls"


@patch("podman_mcp.server.subprocess.run")
def test_secret_create(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.secret_create("mypassword", "s3cr3t")
    assert "secret create" in cmd(mock_sub)
    assert "mypassword" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_secret_remove(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.secret_remove("mypassword")
    assert cmd(mock_sub) == "podman secret rm mypassword"


@patch("podman_mcp.server.subprocess.run")
def test_secret_inspect(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.secret_inspect("mypassword")
    assert cmd(mock_sub) == "podman secret inspect mypassword"


# ---------------------------------------------------------------------------
# Generate
# ---------------------------------------------------------------------------

@patch("podman_mcp.server.subprocess.run")
def test_generate_kube(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.generate_kube("mypod")
    assert cmd(mock_sub) == "podman generate kube mypod"


@patch("podman_mcp.server.subprocess.run")
def test_generate_systemd(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.generate_systemd("mycontainer")
    assert "generate systemd" in cmd(mock_sub)
    assert "mycontainer" in cmd(mock_sub)


# ---------------------------------------------------------------------------
# System
# ---------------------------------------------------------------------------

@patch("podman_mcp.server.subprocess.run")
def test_system_info(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.system_info()
    assert cmd(mock_sub) == "podman system df"


@patch("podman_mcp.server.subprocess.run")
def test_system_prune(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.system_prune()
    assert "system prune -f" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_system_prune_all(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.system_prune(all=True)
    assert "-a" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_podman_version(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.podman_version()
    assert cmd(mock_sub) == "podman version"


@patch("podman_mcp.server.subprocess.run")
def test_podman_info(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.podman_info()
    assert cmd(mock_sub) == "podman info"


@patch("podman_mcp.server.subprocess.run")
def test_system_events_no_filters(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.system_events()
    assert "events --stream=false" in cmd(mock_sub)


@patch("podman_mcp.server.subprocess.run")
def test_system_events_with_filters(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.system_events(since="1h", until="now", filter="event=start")
    c = cmd(mock_sub)
    assert "--since 1h" in c
    assert "--until now" in c
    assert "--filter event=start" in c


@patch("podman_mcp.server.subprocess.run")
def test_login_registry(mock_sub):
    mock_sub.return_value = mock_subprocess()
    server.login_registry("registry.example.com", "user", "pass")
    c = cmd(mock_sub)
    assert "login" in c
    assert "registry.example.com" in c
    assert "-u user" in c
    assert "-p pass" in c


# ---------------------------------------------------------------------------
# Return value
# ---------------------------------------------------------------------------

@patch("podman_mcp.server.subprocess.run")
def test_returns_stdout(mock_sub):
    mock_sub.return_value = mock_subprocess(stdout="IMAGE ID")
    result = server.list_images()
    assert result == "IMAGE ID"


@patch("podman_mcp.server.subprocess.run")
def test_returns_stderr_when_no_stdout(mock_sub):
    mock_sub.return_value = mock_subprocess(stdout="", stderr="Error: no such image")
    result = server.pull_image("nonexistent:latest")
    assert result == "Error: no such image"
