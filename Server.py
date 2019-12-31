'''
    This is the Server side of a chat application.
    Based on the work from:
        https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
'''

import socket
from threading import Thread

def accept_incomming():
    '''
        Runs an infinate loop in it's own Thread listening for incoming connections.
        Adds to a dict, where the key(client) is the socket object, and value(address) is the address of the far end.
        Creates a new thread for each new conneciton.
    '''
    while True:
        client, address = server.accept()
        addresses[client] = address
        Thread(target=handle_client, args=(client,)).start()
        
def handle_client(client):
    '''
        Sets the Username to the first string that comes over the connection.
        Sends back a welcome message.
        Broadcast to all connected users the a new user has joined.
        Adds the new users to a dict where the key(client) is a socket object, and the value(name) is the username.
        Creates a loop that broadcasts incomming messages.
        If incoming message is "/quit": 
            closes the connection
            removes the dict entry
            sends a broadcast telling everyone the Users has left the channel
    '''
    name = client.recv(BUFFER_SIZE).decode('utf-8')
    welcome = f"Welcome {name}. When you want to quit send a /quit command."
    client.send(bytes(welcome, 'utf-8'))
    msg = f"{name} has joined the channel."
    broadcast(bytes(msg, 'utf-8'))
    clients[client] = name
    
    while True:
        try:
            msg = client.recv(BUFFER_SIZE)
        except ConnectionResetError:
            continue
        if msg != bytes("/quit", 'utf-8'):
            broadcast(msg, name+": ")
        else:
            try:
                client.send(bytes("/quit", 'utf-8'))
            except ConnectionResetError:
                continue
            client.close()
            del clients[client]
            broadcast(bytes(f"{name} has left the channel", 'utf-8'))
            break
        
def broadcast(msg, prefix=""):
    '''
        Sends a message to all users in the clients dict.
    '''
    for sock in clients:
        sock.send(bytes(prefix, 'utf-8')+ msg)


if __name__ == "__main__":
    '''
        Creats the addresses and clients dictionaries.
        Sets the Server's IP, Port, and Buffer size.
        Creates the socket, binds it to the ip:port.
        Sets the socket to listen for up to 10 active users.
        Creates and Starts the Thread to listen for incomming connections.
    '''
    addresses = {}
    clients = {}
    
    server_IP = "127.0.0.1"
    TCP_Port = 1234
    BUFFER_SIZE = 1024
    ADDR = (server_IP, TCP_Port)
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    server.listen(10)
    ACCEPT_THREAD = Thread(target=accept_incomming)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()