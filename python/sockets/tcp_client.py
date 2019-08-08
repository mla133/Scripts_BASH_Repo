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

# Example string sent to THMI:
# in:0249{"h":["d9","05","f4","2c","a8","43","fe","e4","ca","48","c4","d2","d7","ca","dd","a5","83","62","ae","be","7b","1e","d9","d2","a7","2b","be","39","0d","40","17","26"],"ts":422510,"seq":31192,"id":"beaglebone","type":"cmd","ins":0,"text":"GET 4"}
