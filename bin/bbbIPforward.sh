#!/bin/bash

# bbbIPforward.sh -- Enable internet access for the BeagleBone Black (BBB)
# using the linux HOST as a router

bbbAddr="192.168.7.2"
hostAddr="192.168.7.1"

# Configure IP forwarding on HOST
sudo iptables -A POSTROUTING -t nat -j MASQUERADE
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward > /dev/null

# copy ssh key to BBB for passwordless logins
ssh-copy-id root@$bbbAddr

# Configure BBB to use HOST as gateway
ssh root@$bbbAddr "/sbin/route add default gw $hostAddr"

# Backup and substitute BBB resolv.conf with HOST resolv.conf
ssh root@$bbbAddr "mv -n /etc/resolv.conf /etc/resolv.conf.bak"
scp /etc/resolv.conf root@$bbbAddr:/etc/
