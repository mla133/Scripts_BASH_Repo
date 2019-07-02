#!/usr/bin/env python

import sys, socket, json

UNIX_FILE = "/dev/shm/Delivery/Misc/in"

#msg = '{"seq":0,"source":14,"priority":5,"qos":2,"command":"Set Alarm","args":["0","Bool_system_alarms","powerfail","",""],"data":""}'
msg = '{"seq":0,"source":14,"priority":5,"qos":2,"command":"Clear Alarm","args":["0","Bool_system_alarms","powerfail","",""],"data":""}'
#msg = '{"seq":0,"source":14,"priority":0,"qos":2,"command":"Set Alarm","args":["2","Bool_arm_alarms","arm_overrun","",""],"data":""}'
#msg = '{"seq":0,"source":14,"priority":0,"qos":2,"command":"Clear Alarm","args":["2","Bool_arm_alarms","arm_overrun","",""],"data":""}'
json_msg = json.dumps(msg)
actual_msg = "%04i" % (sys.getsizeof(json_msg)-10) + msg
print msg
print json_msg
print actual_msg

try:

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect(UNIX_FILE)
    s.sendall(actual_msg)
    s.close()
    s = None
    print "Done writing to %s" % UNIX_FILE

except socket.timeout:
    print "Timed out when connecting to %s" % UNIX_FILE
    s.close
    s = None

except socket.error:
    print "Error when connecting to %s" % UNIX_FILE
    s.close
    s = None

# Example strings for reference
#msg = '0183{"seq":0,"source":14,"priority":5,"qos":2,"command":"Set Alarm","args":["0","Bool_system_alarms","powerfail","",""],"data":""}'
#actual_msg = '{"seq":0,"source":14,"priority":5,"qos":2,"command":"Set Alarm","args":["0","Bool_system_alarms","powerfail","",""],"data":""}'
#msg2 = '0182{"seq":0,"source":14,"priority":0,"qos":2,"command":"Set Alarm","args":["2","Bool_arm_alarms","arm_overrun","",""],"data":""}'
#actual_msg2 = '{"seq":0,"source":14,"priority":0,"qos":2,"command":"Set Alarm","args":["2","Bool_arm_alarms","arm_overrun","",""],"data":""}'

#print("Num of char in '"+actual_msg+"' = "+str(len(actual_msg)))
#print("Memory size of '"+actual_msg+"' = "+str(sys.getsizeof(actual_msg))+ " bytes")
#print
#print("Num of char in '"+actual_msg2+"' = "+str(len(actual_msg2)))
#print("Memory size of '"+actual_msg2+"' = "+str(sys.getsizeof(actual_msg2))+ " bytes")


