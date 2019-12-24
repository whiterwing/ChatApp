import socket

server_IP = "127.0.0.1"
server_Port = 1234
BUFFER_SIZE = 1024
username = input(f"Username: ")
send_Data = f"username says: {username}"


server = socket.create_connection((server_IP, server_Port))
server.send(send_Data.encode('utf-8'))

while True:
    message = input(f"{username} says: ")
    
    server.send((f"{username} says: " + message).encode("utf-8"))
    
    if message == "exit":
        server.close()
        break
    
    data = server.recv(BUFFER_SIZE)
    print (str(data)[2:len(str(data))-1])