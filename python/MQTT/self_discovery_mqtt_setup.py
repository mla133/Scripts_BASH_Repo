PORT = 7000
GROUP = 'ff15:7079:7468:6f6e:6465:6d6f:6d63:6173'

import os
import time
import struct
import socket
import sys
import json
import mosquitto

def server():
    print ("Server")
    address = socket.getaddrinfo(GROUP, None)[0] #Get the IPv6 Link Local Address from the board
    my_socket = socket.socket(address[0], socket.SOCK_DGRAM) #Establish a socket connection
    broker_ip = 'fe80::d239:72ff:fe18:42a8%eth0'

    my_client = mosquitto.Mosquitto("Controller", False) #Instantiate a client that wants a persistent connection with the broker with unique id Meter 1
    my_client.on_connect = connection_response
    my_client.on_message = message_received #Bind the on_message callback to function message_received
    my_client.on_subscribe = subscribe_response #Bind the on_subscribe callback to function subscribe_response
    #my_client.on_publish = message_published
    my_client.connect(broker_ip) #Establish the connection with the broker
    my_client.subscribe("station01/AcculoadIV/json/systemSetup", qos=1) #Subscribe to topic station01/AcculoadIV/arm1/json/test2 with QoS = 1

    count = 0
    while True:
        count = count + 1
        data = {
                    "Assignment" : count
                }

        my_socket.sendto("Test", (address[4][0], PORT)) #"Broadcast" the IPv6 Link Local Address over the PORT specified above for the clients to receive along with data "Test"
        my_client.publish("station01/AcculoadIV/json/systemAssignment", json.dumps(data), qos=1)
        my_client.loop_start() #Start MQTT loop
        time.sleep(10) #Send the message out every 10 seconds

def receiver():
    print ("Client")
    address = socket.getaddrinfo(GROUP, None)[0] #Get the IPv6 Link Local Address from the board
    my_socket = socket.socket(address[0], socket.SOCK_DGRAM) #Establish a socket connection
    my_socket.bind(('', PORT)) #Bind to the PORT specified above

    group = socket.inet_pton(address[0], address[4][0])
    request = group + struct.pack('@I', 0) #Build the request to request to join the group

    my_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, request) #Join the GROUP specified above

    server_info = None

    while server_info == None:
        server_info = my_socket.recvfrom(1500) #Wait until the server IPv6 Address is received

    broker_ip = server_info[1][0] #Pull the IP address out of the message sent by the server
    mqtt(broker_ip) #Pass the broker_ip address to auto configure MQTT

def connection_response(self, userdata, response):
    if response == 0:
        connection = "Connection Accepted"
    elif response == 1:
        connection = "Connection Refused, Unacceptable Protocol Version"
    elif response == 2:
        connection = "Connection Refused, Identifier Rejected"
    elif response == 3:
        connection = "Connection Refused, Server Unavailable"
    elif response == 4:
        connection = "Connection Refused, Bad User Name or Password"
    elif response == 5:
        connection = "Connection Refused, Not Authorized"

    print(connection)

def message_received(client, userdata, message):
    print("Meter 1 State:")
    print(message.payload) #Print out the message contents when received from the broker (from the topic subscribed to)
    print("QoS = " + str(message.qos)) #Print out the QoS

def subscribe_response(client, userdata, mid, granted_qos): 
    print("Subscribed")
    #print("QoS = " + str(granted_qos[0]))
    #print("Mid = " + str(mid))
    #print("User Data: " + str(userdata))

#def message_published(client, userdata, mid):
#    print("Message Published")

def mqtt(broker_ip):
    my_client = mosquitto.Mosquitto("A4B", True) #Instantiate a client that wants a persistent connection with the broker with unique id Meter 1
    my_client.on_connect = connection_response
    my_client.on_message = message_received #Bind the on_message callback to function message_received
    my_client.on_subscribe = subscribe_response #Bind the on_subscribe callback to function subscribe_response
    #my_client.on_publish = message_published
    my_client.connect(broker_ip) #Establish the connection with the broker
    my_client.subscribe("station01/AcculoadIV/json/systemAssignment", qos=1) #Subscribe to topic station01/AcculoadIV/arm1/json/test2 with QoS = 1

    data = {
            "device" : "A4B"
           }
    while True: #Keep checking for messages that were published to the topic
        time.sleep(5)
        my_client.publish("station01/AcculoadIV/json/systemSetup", json.dumps(data), qos=1) #Publish data to topic station01/AcculoadIV/arm1/json/test1 with QoS = 1
        my_client.loop_start() #Start MQTT loop

#Check command line arguments to determine if the device is a server or a client
if "-s" in sys.argv[1:]:
    server()
elif "-c" in sys.argv[1:]:
    receiver()