# ansible-role-guacamole #

[![Build Status](https://travis-ci.com/cisagov/ansible-role-guacamole.svg?branch=develop)](https://travis-ci.com/cisagov/ansible-role-guacamole)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/cisagov/ansible-role-guacamole.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/ansible-role-guacamole/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/cisagov/ansible-role-guacamole.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/ansible-role-guacamole/context:python)

An Ansible role for installing guacamole

NOTE: SSM passwords must be setup before deployment

## Requirements ##

None.

## Role Variables ##

None.

## Dependencies ##

Docker is a dependency found here:

```yaml
dependencies:
  - src: https://github.com/cisagov/ansible-role-docker
    name: docker
```

## Example Playbook ##

Here's how to use it in a playbook:

```yaml
- hosts: all
  become: yes
  become_method: sudo
  roles:
    - guacamole
```

## Contributing ##

We welcome contributions!  Please see [here](CONTRIBUTING.md) for
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

Kyle Evers - <kyle.evers@trio.dhs.gov>
