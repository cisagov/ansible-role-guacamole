"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize(
    "d, perms",
    [
        ("/var/guacamole", 0o755),
        ("/var/guacamole/httpd/ssl", 0o755),
    ],
)
def test_directories(host, d, perms):
    """Test that the expected directories were created and are not empty."""
    assert host.file(d).exists, f"Directory {d} does not exist"
    assert host.file(d).is_directory, f"{d} is not a directory"
    assert host.file(d).listdir(), f"Directory {d} is empty"
    assert host.file(d).mode == perms, f"Directory {d} does not have mode {perms:#o}"


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
    assert host.file(f).exists, f"File {f} does not exist"
    assert host.file(f).is_file, f"{f} is not a file"
    assert host.file(f).content, f"File {f} is empty"
    assert host.file(f).mode == perms, f"File {f} does not have mode {perms:#o}"


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
    assert host.file(link).exists, f"Link {link} does not exist"
    assert host.file(link).is_symlink, f"{link} is not a symlink"
    assert host.file(link).linked_to == target, f"Link {link} does not link to {target}"


def test_services(host):
    """Test that the expected services were enabled."""
    assert host.service(
        "guacamole-composition"
    ).is_enabled, "guacamole-composition service is not enabled"


@pytest.mark.parametrize(
    "image",
    [
        "cisagov/guacscanner:1.2.2",
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
    ), f"Docker image {image} is not present"
