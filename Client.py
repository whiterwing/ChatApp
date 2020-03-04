'''
    This is the Client side of a chat application.
    Based on the work from:
        https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
'''

import asyncio

class network_Handle(object):
    '''
    This class is for the network portion of the application.
    '''
    def __init__(self):
        
        self.server_IP = "127.0.0.1"
        self.server_Port = 1234
        
        asyncio.get_event_loop().create_task(self.server_connect())
        
    async def server_connect(self):
        try:
            self.chat_reader, self.chat_writer = await asyncio.open_connection(self.server_IP, self.server_Port)
            print(f"Connected to server at {self.server_IP}:{self.server_Port}")
        except:
            print("Server not found.")
    
    async def receive(self):
        '''
            Runs an infinate loop in it's own thread started from network_Handle.__init__, listening for
            messages from the server to add to the Chatbox's message log.
        '''
        msg = await self.chat_reader.read(1024)
        print(f"Received {msg.decode()!r}")
        return msg
            
                
    def send(self, msg):
        '''
            Pulls the String out of Chatbox.my_msg, and makes sure it's not an empty string.
            Clears the chat input box.
            Sends the message to the Server.
            If the message is "/quit", closes the socket, and exits the GUI.
        '''
        self.chat_writer.write(msg.encode())
        if msg == "/quit":
            asyncio.get_event_loop().create_task(self.close_connection())
            print("connection closed.")
            
            
    async def close_connection(self):
        self.chat_writer.close()
        await self.chat_writer.wait_closed()

if __name__ == "__main__":
    '''
        Starts the application.
    '''
    Network = network_Handle()