"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os
import re

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("d", ["/var/guacamole", "/var/guacamole/httpd/ssl"])
def test_directories(host, d):
    """Test that the expected directories were created and are not empty."""
    assert host.file(d).exists
    assert host.file(d).is_directory
    assert host.file(d).listdir()
    assert host.file(d).mode == 0o755


@pytest.mark.parametrize(
    "f, perms",
    [
        ("/etc/pam.d/guacamole", 0o644),
        ("/etc/pam.d/guacamole-admin", 0o644),
        ("/var/guacamole/httpd/ssl/self.cert", 0o644),
        ("/var/guacamole/httpd/ssl/self-ssl.key", 0o644),
        ("/etc/apache2/sites-available/guacamole.conf", 0o644),
        ("/usr/local/sbin/02_setup_guacamole_services.sh", 0o500),
    ],
)
def test_files(host, f, perms):
    """Test that the expected files were created and are non-empty."""
    assert host.file(f).exists
    assert host.file(f).is_file
    assert host.file(f).content
    assert host.file(f).mode == perms


@pytest.mark.parametrize(
    "link, target",
    [
        (
            "/etc/apache2/sites-enabled/guacamole.conf",
            "/etc/apache2/sites-available/guacamole.conf",
        )
    ],
)
def test_links(host, link, target):
    """Test that the expected links were created and point to the correct place."""
    assert host.file(link).exists
    assert host.file(link).is_symlink
    assert host.file(link).linked_to == target


def test_services(host):
    """Test that the expected services were enabled."""
    assert host.service("guacamole-composition").is_enabled


def test_dropin_dir(host):
    """Test that the httpd drop-in directory was created as expected."""
    f = host.file("/etc/systemd/system/apache2.service.d")

    assert f.exists
    assert f.is_directory
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o755


def test_dropin_file(host):
    """Test that the httpd drop-in file was created as expected."""
    f = host.file("/etc/systemd/system/apache2.service.d/apache2.conf")

    assert f.exists
    assert f.is_file
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o644


@pytest.mark.parametrize(
    "prop,regex",
    [
        ("After", r"^After=.*cloud-final\.service"),
    ],
)
def test_unit_properties(host, prop, regex):
    """Test that unit properties were modified via drop-ins as expected."""
    cmd = f"systemctl show --no-pager --property={prop} apache2.service"
    cmd_result = host.run(cmd)
    assert cmd_result.rc == 0, f"{cmd} command failed"
    assert (
        re.search(regex, cmd_result.stdout) is not None
    ), f"Regex {regex} does not match any line in {cmd} output."


@pytest.mark.parametrize(
    "image",
    [
        "cisagov/guacscanner:1.2.1",
        "guacamole/guacd:1.6.0",
        "guacamole/guacamole:1.6.0",
        "postgres:18",
    ],
)
def test_docker_images_pulled(host, image):
    """Test that Docker images used by Guacamole Docker composition are present."""
    assert image in host.check_output(
        # Unfortunately Jinja and Go templates use the same
        # double-bracket syntax, so we have to force Jinja to ignore
        # it so the Go template gets passed along to the docker
        # command.
        "docker images --format='{% raw %}{{.Repository}}:{{.Tag}}{% endraw %}'"
    )
