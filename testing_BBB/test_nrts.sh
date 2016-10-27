#!/bin/sh


echo ".timeout 10000" > /tmp/commands.sql
echo ".headers ON" >> /tmp/commands.sql
echo ".mode line" >> /tmp/commands.sql
echo "select * from prove_inj;" >> /tmp/commands.sql 
echo "select * from alarm_log where alarm_set_cleared=1 AND ( (lower(alarm_table_name)='bool_system_alarms' AND (alarm_arm_no = 0 OR alarm_arm_no = $1) ) OR (lower(alarm_table_name) ='bool_injector_alarms' AND alarm_offset = $2));" >> /tmp/commands.sql
echo ".quit" >> /tmp/commands.sql
sqlite3 /dev/shm/accu4_db_ram.sqlite < /tmp/commands.sql
#rm -rf /tmp/commands.sql
