cript to start all processes for Revelation

#export needed environment vars for Qt app to use touchscreen input

export TSLIB_TSDEVICE='/dev/input/event0'
export TSLIB_CALIBFILE='/etc/pointercal'
export TSLIB_CONFFILE='/etc/ts.conf'
export LD_LIBRARY_PATH='/lib/ts'

export QWS_MOUSE_PROTO='tslib'
export QWS_DISPLAY="LinuxFb:mmWidth120:mmHeight90"
export $(dbus-launch)
#launch application processes
echo "Starting Delivery Application"
printer_daemon >/dev/null 2>&1&
revelation > /dev/null 2>&1&
#echo "Changing Permissions of Databases, sleep 10 seconds"
#sleep 10 
chown www-data /dev/shm/Revel_db_ram.sqlite
chown www-data /dev/shm/pdb_edit_buf.sqlite
chmod 666 /dev/shm/Revel_db_ram.sqlite
chmod 666 /dev/shm/pdb_edit_buf.sqlite
echo "Starting GUI Application"
QtGUI -qws localhost/index.html > /dev/null 2>&1&
#QtGUI -qws -nograb localhost > /dev/null 2>&1&
echo "Printing System Information"
ifconfig eth0 | grep "inet addr" | gawk -F: '{print $2}' | gawk '{print $1}' > /var/tmp/IP.txt
ifconfig eth0 | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}' > /var/tmp/MAC.txt

