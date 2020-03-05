'''
    This is the Client side of a chat application.
'''

import asyncio

class network_Handle(object):
    '''
    This class is for the network portion of the application.
    '''
    def __init__(self):
        '''
            defines the server's IP and Port. Starts the server_connection coroutine.
        '''
        self.server_IP = "127.0.0.1"
        self.server_Port = 1234
        
        asyncio.get_event_loop().create_task(self.server_connect())
        
    async def server_connect(self):
        '''
            tries to connect to the server, and defines the readerStream/writerStream.
        '''
        try:
            self.chat_reader, self.chat_writer = await asyncio.open_connection(self.server_IP, self.server_Port)
            print(f"Connected to server at {self.server_IP}:{self.server_Port}")
        except:
            print("Server not found.")
    
    async def receive(self):
        '''
            Waits for a message from the server, decodes and send the message to the GUI.
        '''
        msg = await self.chat_reader.read(1024)
        print(f"Received {msg.decode()!r}")
        return msg.decode()
            
                
    def send(self, msg):
        '''
            Receives a Message to send to the server via the writerStream.
            If the user wants to quit starts a coroutine to close the connection
        '''
        self.chat_writer.write(msg.encode())
        if msg == "/quit":
            asyncio.get_event_loop().create_task(self.close_connection())
            print("connection closed.")
            
            
    async def close_connection(self):
        '''
            A coroutine for closing out the connection to the server.
        '''
        self.chat_writer.close()
        await self.chat_writer.wait_closed()

if __name__ == "__main__":
    '''
        Starts the network handler.
    '''
    Network = network_Handle()