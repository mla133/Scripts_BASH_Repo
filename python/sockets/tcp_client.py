#!/usr/bin/env python

import sys, socket, json, time


#TCP_IP = '127.0.0.1'
TCP_IP = '192.168.180.86' 
#TCP_PORT = 5005
TCP_PORT = 6083
BUFFER_SIZE = 1024
#MESSAGE = 'GET 4'
epoch_time = int(time.time())
print epoch_time

MESSAGE = '{"ts": %d, "seq": 1, "id": "beaglebone", "type": "cmd", "ins": 0, "text":"GET 4"}' % epoch_time
json_msg = json.dumps(MESSAGE)

print MESSAGE
print json_msg

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(json_msg)
data = s.recv(BUFFER_SIZE)
s.close()

print "received data:", data
