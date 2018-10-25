#!/bin/bash
# Might need to be run as root

echo -e "\e[35;40mBacking up Matt's BBB\e[0m"
./backup_db.sh 192.168.181.206
echo -e "\e[35;40mBacking up Jason's BBB\e[0m"
./backup_db.sh 192.168.181.171
echo -e "\e[35;40mBacking up Ian's BBB\e[0m"
./backup_db.sh 192.168.181.191
echo -e "\e[35;40mBacking up Paul's BBB\e[0m"
./backup_db.sh 192.168.181.200
echo -e "\e[35;40mBacking up Ankita's BBB\e[0m"
./backup_db.sh 192.168.180.36
echo -e "\e[35;40mBacking up Tenger's BBB\e[0m"
./backup_db.sh 192.168.181.182
