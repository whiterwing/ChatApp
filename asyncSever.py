# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 08:44:45 2020

@author: white
"""


import asyncio

async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')
    print (f"{addr} connected.")
    
    data = await reader.read(1024)
    message = data.decode()
    
    print (f"Received {message!r} from {addr!r}")
    
    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()
    
    print("Close the connection")
    writer.close()
    
async def main():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)
    
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")
    
    async with server:
        await server.serve_forever()
        
asyncio.get_event_loop().create_task(main())