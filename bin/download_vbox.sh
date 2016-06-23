#!/bin/bash
wget -b http://download.virtualbox.org/virtualbox/4.3.26/virtualbox-4.3_4.3.26-98988~Ubuntu~lucid_i386.deb
wget -b http://download.virtualbox.org/virtualbox/4.3.26/Oracle_VM_VirtualBox_Extension_Pack-4.3.26-98988.vbox-extpack
echo "Use <tail -f wget-log> to view download status"
echo "When finished, use <dpkg -i virtualbox-4.3_4.3.26-98988~Ubuntu~lucid_i386.deb>"
