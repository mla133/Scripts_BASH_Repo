#!/usr/bin/env python

import socket

UNIX_FILE = "/home/root/in"
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#s.bind((UNIX_FILE))
s.bind('/home/root/in')
s.listen(1)

conn, addr = s.accept()
print 'Connection file: ', UNIX_FILE
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "server received data:", data
    conn.send(data)  # echo
conn.close()
