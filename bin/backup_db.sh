#!/bin/bash
# Might need to be run as root

if [ -z "$1" ]; then
  echo -e "\e[31;40mUsage: $0 IP_ADDRESS\e[0m"
  exit
fi

IP=$1
DATE_STAMP=$(date +%Y%m%d_%H%M%S)
echo -e "\e[32;40mPulling version-fmc from:\e[0m \e[33;40m$IP\e[0m"

BBB_VERSION=$(ssh root@$IP "cat /etc/version-fmc" | cut -d- -f2-4)
DEST=~/accu4_db/$IP/$BBB_VERSION/$DATE_STAMP

# Point to all the BeagleBone databases to be backed up
PDB_BUF=/dev/shm/pdb_edit_buf.sqlite
ACCU4_DB=/media/data/database/accu4_db.sqlite
DATALOG=/media/data/database/accu4_datalog.sqlite

# Version control of BBB Image...
echo -e "\e[32;40mVersion:\e[0m \e[33;40m$BBB_VERSION\e[0m"

echo -e "\e[32;40mCreating directories for databases...\e[0m"
mkdir -pv $DEST 	# ~/accu4_db/<ip>/version/timestamp

# SCP the databases to the destination on the host
echo -e "\e[32;40mPulling databases to the host...please wait...\e[0m"
scp root@$IP:$PDB_BUF $DEST
scp root@$IP:$DATALOG $DEST
scp root@$IP:$ACCU4_DB $DEST
