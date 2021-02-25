#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

# This script is intended to set up the guacamole and guacamole-admin
# FreeIPA services on this host.  It creates these services if they do
# not already exist.
#
# These variables must be set before client installation:
#
# hostname: The hostname of this IPA client (e.g. client.example.com).

# The file installed by cloud-init that contains the value for the
# above variables.
freeipa_vars_file=/var/lib/cloud/instance/freeipa-vars.sh

# Load above variable from a file installed by cloud-init:
if [[ -f "$freeipa_vars_file" ]]
then
  # Disable this warning since the file is only available at runtime
  # on the server.
  #
  # shellcheck disable=SC1090
  source "$freeipa_vars_file"
else
  echo "FreeIPA variables file does not exist: $freeipa_vars_file"
  echo "It should have been created by cloud-init at boot."
  exit 254
fi

# Get the default Ethernet interface.
#
# Returns the default Ethernet interface.
function get_interface {
  ip route | grep default | sed "s/^.* dev \([^ ]*\).*$/\1/"
}

# Get the IP address corresponding to an interface.
#
# Parameters:
# $1 - the interface name
#
# Returns the IP address corresponding to the specified interface.
function get_ip {
  ip --family inet address show dev "$1" | \
    grep --perl-regexp --only-matching 'inet \K[\d.]+'
}

# Create the FreeIPA service if it does not already exist.
#
# Parameters:
# $1 - the service name
function create_service_if_needed {
  # Since the service may not be found, which returns an error code,
  # we need to temporarily turn off errexit for this.
  set +o errexit
  # hostname is defined in the FreeIPA variables file that is
  # sourced toward the top of this file.  Hence we can ignore the
  # "undefined variable" warning from shellcheck.
  #
  # shellcheck disable=SC2154
  ipa service-find --canonical-principal="$1/$hostname"
  rc=$?
  set -o errexit
  if [[ $rc -ne 0 ]]
  then
    ipa service-add "$1/$hostname"
    # Grab our IP address
    interface=$(get_interface)
    ip_address=$(get_ip "$interface")
    ip_address_dashes=${ip_address//./-}
    # Add an alias that is the PTR record as determined from the
    # Shared Services VPC.
    ipa service-add-principal "$1/$hostname" "$1/ip-${ip_address_dashes}.ec2.internal"
  fi
}

# Create the guacamole services, if needed.
create_service_if_needed "guacamole"
create_service_if_needed "guacamole-admin"
