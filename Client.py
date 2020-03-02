'''
    This is the Client side of a chat application.
    Based on the work from:
        https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
'''

import socket
import queue
import asyncio
import sys

class network_Handle(object):
    '''
    This class is for the network portion of the application.
    '''
    msg_recv = queue.Queue()
    msg_send = queue.Queue()
    def __init__(self):
        '''
        Sets Chatbox and top to global vars.
        Sets the server's ip and which port to use, and the buffer size to send across the network.
        Trys to create the connection to the server, if the server can't be found, exits the script.
        Starts the thread for receiving messages from the server.
        '''
        server_IP = "127.0.0.1"
        server_Port = 1234
        self.ADDR = (server_IP,server_Port)
        self.BUFFER_SIZE = 1024
        
        self.server_connect()
        
    def server_connect(self):
        try:
            self.client_socket = socket.create_connection(self.ADDR)
            self.client_socket.setblocking(0)
            print(f"Connected to server at {self.ADDR}")
        except ConnectionRefusedError:
            print("No Server Found.")
            sys.exit()
        
    
    async def receive(self):
        '''
            Runs an infinate loop in it's own thread started from network_Handle.__init__, listening for
            messages from the server to add to the Chatbox's message log.
        '''
        print("Starting receiver.")
        while True:
            await asyncio.sleep(1/30)
            try:
                msg = (self.client_socket.recv(self.BUFFER_SIZE).decode('utf-8'))
                print(f"Received {msg}")
                self.msg_recv.put(msg)
            except BlockingIOError:
                pass
            except OSError:
                break
                
    async def send(self):
        '''
            Pulls the String out of Chatbox.my_msg, and makes sure it's not an empty string.
            Clears the chat input box.
            Sends the message to the Server.
            If the message is "/quit", closes the socket, and exits the GUI.
        '''
        print("Starting Sender.")
        while True:
            await asyncio.sleep(1/30)
            try:
                msg = self.msg_send.get_nowait()
                self.client_socket.send(bytes(msg, 'utf-8'))
                if msg=="/quit":
                    self.client_socket.close()
            except queue.Empty:
                pass

if __name__ == "__main__":
    '''
        Starts the application.
    '''
    Network = network_Handle()