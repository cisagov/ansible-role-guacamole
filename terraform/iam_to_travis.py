#!/usr/bin/env python

import json
import subprocess
import sys


def creds_from_child(child_module):
    for resource in child_module["resources"]:
        if resource["address"] == "aws_iam_access_key.key":
            key_id = resource["values"]["id"]
            secret = resource["values"]["secret"]
            return key_id, secret
    return None, None


def creds_from_terraform():
    c = subprocess.run("terraform show -json", shell=True, stdout=subprocess.PIPE)
    j = json.loads(c.stdout)

    for child_module in j["values"]["root_module"]["child_modules"]:
        key_id, secret = creds_from_child(child_module)
        if key_id:
            return key_id, secret
    else:
        return None, None


def wrap_for_yml(s, length=75):
    result = []
    while True:
        result.append(s[:length])
        s = s[length:]
        if not s:
            break
        # indent
        s = "      " + s
    return "\\\n".join(result)


def encrypt_for_travis(variable_name, value):
    command = f'travis encrypt --com --no-interactive "{variable_name}={value}"'
    c = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    s = f"    - secure: {c.stdout.decode('utf-8')}"
    print(f"    # {variable_name}")
    print(wrap_for_yml(s))


def main():
    key_id, secret = creds_from_terraform()
    if key_id is None:
       print("creds not found")
       sys.exit(-1)

    encrypt_for_travis("AWS_ACCESS_KEY_ID", key_id)
    encrypt_for_travis("AWS_SECRET_ACCESS_KEY", secret)

    return 0


if __name__ == "__main__":
    sys.exit(main())
