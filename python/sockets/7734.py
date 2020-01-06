#!/usr/bin/env python

import sys, socket, json, time


TCP_IP = '192.168.181.76' 
TCP_PORT = 7734 
BUFFER_SIZE = 1024

MESSAGE =  b'*EQ\r\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.sendall(b'*01ET\r\n')
data = s.recv(BUFFER_SIZE)
s.close()

print("received data:", data)
