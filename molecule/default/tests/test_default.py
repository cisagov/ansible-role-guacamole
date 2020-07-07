"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

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
        ("/usr/local/sbin/setup_guacamole_services.sh", 0o700),
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


def test_apache2_unit_modification(host):
    """Test that the apache2 httpd unit file was modified as expected."""
    assert host.file("/lib/systemd/system/apache2.service").contains(
        r"After=.* cloud-final.service"
    )
