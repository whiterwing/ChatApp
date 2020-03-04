# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 07:35:17 2020

@author: white
"""


import asyncio

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    
    print(f"Send: {message!r}")
    writer.write(message.encode())
    
    data = await reader.read()
    print(f"Received: {data.decode()!r}")
    
    print("close the connection")
    writer.close()
    
asyncio.get_event_loop().create_task(tcp_echo_client("Hello!"))