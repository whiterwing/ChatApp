'''
    This is the Server side of a chat application.
    Based on the work from:
        https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
'''
import asyncio

class Server:
    def __init__(self):
        '''
            defines the Server's IP and Port, creates a dictionary for all
            connections. Starts the server.
        '''
        self.connections = {}
        self.server_IP = "127.0.0.1"
        self.TCP_port = 1234

        self.loop = asyncio.get_event_loop()

        self.loop.create_task(self.accecpt_connection())
    
    async def accecpt_connection(self):
        '''
            creates a coroutine to wait for incoming connections, and starts an
            instance of client_handler when one does. The client_handler is passed
            the readerStream/writerStream objects.
        '''
        self.server = await asyncio.start_server(
            self.client_handler, self.server_IP, self.TCP_port)
        await self.server.serve_forever()

    async def client_handler(self, reader, writer):
        '''
            A coroutine for handling the client connections. Receives a username
            from the client, checks if the username is already used, sends a welcome
            message. Addes the user to the connections dictionary with the name as the key
            and the I/O streams as the value. Let's all other users know who has connected.
            Waits for messages the connected client, broadcasts the message back to everyone
            else connected. If the user wants to quit, starts the close_connection coroutine.
        '''
        while True:
            name = await reader.read(1024)
            name = name.decode()
            if name not in self.connections.keys():
                writer.write(f"Welcome to the server {name}.".encode())
                break
            else:
                writer.write(f"{name} is already taken.".encode())
                
        
        await self.loop.create_task(self.broadcast(f"{name} has joined the server."))
        await asyncio.sleep(1)
        
        self.connections[name] = writer
        
        await self.loop.create_task(self.onlineBroadcast())
        
        while True:
            data = await reader.read(1024)
            data = data.decode()
            
            if data == "/quit":
                await self.close_connection(writer)
                self.connections.pop(name)
                self.loop.create_task(self.broadcast(f"{name} has left the server."))
                
                await self.loop.create_task(self.onlineBroadcast())
                await asyncio.sleep(1)
                
                break
            else:
                data = f"{name}: {data}"
                self.loop.create_task(self.broadcast(data))
                
    async def onlineBroadcast(self):
        '''
            Makes a STR of everyone connected and sends it to the clients.
        '''
        userstr = "$$$SERVER$$$"
        for user in self.connections.keys():
            userstr += f":{user}"
        self.loop.create_task(self.broadcast(f"{userstr}"))
                
    async def broadcast(self, msg):
        '''
            Sends a message back out to all other connected clients.
        '''
        try:
            for user in self.connections.keys():
                self.connections[user].write(msg.encode())
                await self.connections[user].drain()
        except ConnectionResetError:
            print(f"{user} has disconnected.")
                
    async def close_connection(self, writer):
        '''
            closes out the requested connection.
        '''
        writer.close()
        await writer.wait_closed()
    
if __name__ == "__main__":
    
    server = Server()