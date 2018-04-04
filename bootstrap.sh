#!/bin/bash

exec > /var/log/system-bootstrap.log
exec 2> /var/log/system-bootstrap.log

source ./config

# Update the system
yum update -y

# Static configure host-only adaptor
nmcli d mod enp0s8 ipv4.address $IPV4

SSH_CONFIG_FILE="/etc/ssh/sshd_config"

set_ssh_option() {
    if [[ $# -ne 2 ]]; then
        echo "Invalid number of arguments for set_ssh_option. Expected 2, got $#" >&2
        exit -1
    fi
    
    OPTION="$1"
    SED_CHANGE="s^.*${OPTION}.*^    ${OPTION} $2^g"
    
    sed -E "${SED_CHANGE}" -i "$SSH_CONFIG_FILE"
    if [[ `cat "$SSH_CONFIG_FILE" | grep "$OPTION"` == "" ]]; then
        echo "    $OPTION $2" >> $SSH_CONFIG_FILE
    fi
}


# SSH config
set_ssh_option "PasswordAuthentication" "no"
set_ssh_option "PermitRootLogin" "without-password"
set_ssh_option "PubKeyAuthentication" "yes"
set_ssh_option "RSAAuthentication" "yes"
set_ssh_option "AuthorizedKeysFile" "/root/.ssh/authorized_keys"

SSH_DIR="$HOME/.ssh"
# Make sure .ssh dir exists
if [ ! -d "$SSH_DIR" ]; then
	mkdir -p "$SSH_DIR"
	chmod 600 "$SSH_DIR"
fi

SSH_KEYSFILE="$SSH_DIR/authorized_keys"
if [ ! -f $SSH_KEYSFILE ]; then
    touch "$SSH_KEYSFILE"
    chmod 600 "$SSH_KEYSFILE"
fi

if [[ `cat $SSH_KEYSFILE | grep "$SSH_KEY"` == "" ]]; then
    echo "$SSH_KEY" >> $SSH_KEYSFILE
fi

systemctl reload sshd

# Ensure SELINUX=disabled and setenforce
sed -E "s/SELINUX=[^ ]+/SELINUX=disabled/g" -i "/etc/selinux/config"
setenforce 0

# Docker firewalls
firewall-cmd --add-port=2377/tcp --permanent
firewall-cmd --add-port=7946/tcp --permanent
firewall-cmd --add-port=7946/udp --permanent
firewall-cmd --add-port=4789/udp --permanent
