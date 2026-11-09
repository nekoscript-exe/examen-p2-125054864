#!/bin/sh
set -eu

mkdir -p /run/sshd /root/.ssh
chmod 700 /root/.ssh

if [ ! -f /root/.ssh/id_ed25519 ]; then
    ssh-keygen -t ed25519 \
        -f /root/.ssh/id_ed25519 \
        -N "" \
        -q
fi

cp /root/.ssh/id_ed25519.pub /root/.ssh/authorized_keys

chmod 600 /root/.ssh/id_ed25519
chmod 600 /root/.ssh/authorized_keys
chmod 644 /root/.ssh/id_ed25519.pub

exec /usr/sbin/sshd -D -e
