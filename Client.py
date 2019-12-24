# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 11:01:42 2019

@author: white
"""

import socket

server_IP = "192.168.1.177"
server_Port = 1234
BUFFER_SIZE = 1024
username = input(f"Username: ")
send_Data = f"username %% {username}"


server = socket.create_connection((server_IP, server_Port))
server.send(send_Data.encode('utf-8'))

while True:
    message = input(f"{username} says: ")
    
    server.send(message.encode("utf-8"))
    
    if message == "exit":
        server.close()
        break
    
    data = server.recv(BUFFER_SIZE)
    print (str(data)[2:len(str(data))-1])