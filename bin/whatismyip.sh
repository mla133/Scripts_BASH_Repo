#!/bin/bash
echo
echo "External IP: "
wget -qO - icanhazip.com
echo "Internal IP: "
ifconfig | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'
echo
wget -qO - icanhazip.com > /tmp/ip_output.txt
mail -s "External IP" "matthew.l.allen@gmail.com" < /tmp/ip_output.txt
/bin/rm /tmp/ip_output.txt

exit 0
