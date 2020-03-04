'''
    This is the Server side of a chat application.
    Based on the work from:
        https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
'''
import asyncio

class Server:
    def __init__(self):
        self.connections = {}
        self.server_IP = "127.0.0.1"
        self.TCP_port = 1234

        self.loop = asyncio.get_event_loop()

        self.loop.create_task(self.accecpt_connection())
    
    async def accecpt_connection(self):
        self.server = await asyncio.start_server(
            self.client_connected, self.server_IP, self.TCP_port)
        await self.server.serve_forever()

    async def client_connected(self, reader, writer):
        # Communicate with the client with
        # reader/writer streams.  For example:
        name = await reader.read(1024)
        name = name.decode()
        writer.write(f"Welcome to the server {name}.".encode())
        
        await self.loop.create_task(self.broadcast(f"{name} has joined the server."))
        
        self.connections[name] = writer
        
        while True:
            data = await reader.read(1024)
            data = data.decode()
            
            if data == "/quit":
                await self.close_connection(writer)
                self.connections.pop(name)
                self.loop.create_task(self.broadcast(f"{name} has left the server."))
                break
            else:
                data = f"{name}: {data}"
                self.loop.create_task(self.broadcast(data))
                
    async def broadcast(self, msg):
        for user in self.connections.keys():
            self.connections[user].write(msg.encode())
            await self.connections[user].drain()
                
    async def close_connection(self, writer):
        writer.close()
        await writer.wait_closed()
    
if __name__ == "__main__":
    
    server = Server()