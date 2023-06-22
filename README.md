# ansible-role-guacamole #

[![GitHub Build Status](https://github.com/cisagov/ansible-role-guacamole/workflows/build/badge.svg)](https://github.com/cisagov/ansible-role-guacamole/actions)
[![CodeQL](https://github.com/cisagov/ansible-role-guacamole/workflows/CodeQL/badge.svg)](https://github.com/cisagov/ansible-role-guacamole/actions/workflows/codeql-analysis.yml)

An Ansible role for installing [cisagov/guacamole-composition](https://github.com/cisagov/guacamole-composition).

## Requirements ##

None.

## Role Variables ##

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| guacamole_composition_version | The version of [cisagov/guacamole-composition](https://github.com/cisagov/guacamole-composition) to use. | `0.1.6` | No |
| postgres_username | The username to use when connecting to the PostgreSQL database that backends Guacamole. | n/a | Yes |
| postgres_password | The password to use when connecting to the PostgreSQL database that backends Guacamole. | n/a | Yes |
| private_ssh_key | The private ssh key to use for SFTP file transfer in Guacamole. | n/a | Yes |
| rdp_username | The username for Guacamole to use when connecting to an instance via RDP. | n/a | Yes |
| rdp_password | The password for Guacamole to use when connecting to an instance via RDP. | n/a | Yes |
| vnc_username | The username for Guacamole to use when connecting to an instance via VNC. | n/a | Yes |
| vnc_password | The password for Guacamole to use when connecting to an instance via VNC. | n/a | Yes |
| windows_sftp_base | The base path for the SFTP directories that Guacamole will use when connecting to a Windows instance via VNC. | n/a | Yes |

## Dependencies ##

- [cisagov/ansible-role-docker](https://github.com/cisagov/ansible-role-docker)
- [cisagov/ansible-role-httpd](https://github.com/cisagov/ansible-role-httpd)

## Example Playbook ##

Here's how to use it in a playbook:

```yaml
- hosts: all
  become: yes
  become_method: sudo
  tasks:
    - name: Install Guacamole
      ansible.builtin.include_role:
        name: guacamole
      vars:
        postgres_username: postgres_user
        postgres_password: postgres_password
        private_ssh_key: dummy_key
        rdp_username: rdp_user
        rdp_password: rdp_password
        vnc_username: vnc_user
        vnc_password: vnc_password
        windows_sftp_base: /C:/Users/vnc_user
```

## Contributing ##

We welcome contributions!  Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.

## Author Information ##

Kyle Evers - <kyle.evers@gwe.cisa.dhs.gov>
