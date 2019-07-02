#!/usr/bin/env python

import socket


UNIX_FILE = "/home/root/in"
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#s.connect((UNIX_FILE))
s.connect('/home/root/in')
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print "received data:", data
