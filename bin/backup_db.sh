#!/bin/bash
# Might need to be run as root

if [ -z "$1" ]; then
  echo usage: $0 IP_ADDRESS
  exit
fi

IP=$1
DATE_STAMP=$(date +%Y%m%d_%H%M%S)
DEST=~/accu4_db/$IP/$DATE_STAMP

# Point to all the BeagleBone databases to be backed up
PDB_BUF=/dev/shm/pdb_edit_buf.sqlite
ACCU4_DB=/var/lib/accu4/accu4_db.sqlite
DATALOG=/var/lib/accu4/accu4_datalog.sqlite

mkdir -pv $DEST 	# ~/accu4_db/<ip>/timestamp

# SCP the databases to the destination on the host
echo Pulling databases to the host...please wait...
scp root@$IP:$PDB_BUF $DEST
scp root@$IP:$DATALOG $DEST
scp root@$IP:$ACCU4_DB $DEST
