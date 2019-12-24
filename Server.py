import socket

server_IP = "127.0.0.1"
TCP_Port = 1234
BUFFER_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_IP, TCP_Port))
print(server)
server.listen(10)
print("Server is listening.")
users = dict()

conn = server.accept()[0]
print ("Connection Address:", conn.getpeername())

def __main__():
    BUFFER_SIZE = 1024
    global users

    while True:
        data = conn.recv(BUFFER_SIZE)
        print (data)
        
        try:
            keyword, data = str(data).split(" says: ")
            if keyword.strip("b'") not in users:
                users[data.strip("'")] = conn
                print (f"{conn.getpeername()[0]} connected with username: {data}")
            elif data == "b''": 
                conn.close()
                server.close()
                break
            else:
                print(f"received data from {users[conn.getpeername()[0]]}:", data)
                conn.send(f"{users[conn.getpeername()[0]]} says: {str(data)[2:len(str(data))-1]}".encode("utf-8"))
        except:
            if data == "b'exit'":
                conn.close()
                server.close()
                break
            elif data == "b''": 
                conn.close()
                server.close()
                break


if __name__ == "__main__":
    __main__()