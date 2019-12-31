import socket
from threading import Thread

def accept_incomming():
    while True:
        client, address = server.accept()
        addresses[client] = address
        Thread(target=handle_client, args=(client,)).start()
        
def handle_client(client):
    name = client.recv(BUFFER_SIZE).decode('utf-8')
    welcome = f"Welcome {name}. When you want to quit send a /quit command."
    client.send(bytes(welcome, 'utf-8'))
    msg = f"{name} has joined the channel."
    broadcast(bytes(msg, 'utf-8'))
    clients[client] = name
    
    while True:
        msg = client.recv(BUFFER_SIZE)
        if msg != bytes("/quit", 'utf-8'):
            broadcast(msg, name+": ")
        else:
            try:
                client.send(bytes("/quit", 'utf-8'))
            except ConnectionResetError:
                continue
            client.close()
            del clients[client]
            broadcast(bytes("{name} has left the channel", 'utf-8'))
            break
        
def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, 'utf-8')+ msg)

addresses = {}
clients = {}

server_IP = "127.0.0.1"
TCP_Port = 1234
BUFFER_SIZE = 1024
ADDR = (server_IP, TCP_Port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


if __name__ == "__main__":
    server.listen(10)
    ACCEPT_THREAD = Thread(target=accept_incomming)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()