# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 07:35:17 2020

@author: white
"""


from autobahn.asyncio.websocket import WebSocketClientProtocol, \
WebSocketClientFactory


class MyClientProtocol(WebSocketClientProtocol):
    
    def onConnect(self, response):
        print(f"Server connected: {response.peer}")
        
    def onConnecting(self, transport_details):
        print(f"Connection; transport details: {transport_details}")
        
    def onOpen(self):
        print("Socket opened")
        
        self.sendMessage(u'Hello'.encode('utf-8'))
        
    def onMessage(self, payload, isBinary):
        if isBinary:
            print(f"Binary message received: {len(payload)} bytes")
        else:
            print(f"Text message received: {payload.decode('utf-8')}")
            
    def onClose(self, wasClean, code, reason):
        print(f"Websocket connection closed: {reason}")
        
    def send(self, msg):
        self.sendMessage(msg.encode('utf-8'))
        
        
if __name__ == '__main__':
    try:
        import asyncio
    except ImportError:
        import trollius as asyncio
        
    factory = WebSocketClientFactory(u"ws://127.0.0.1:1234")
    factory.protocol = MyClientProtocol
    
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, '127.0.0.1', 1234)
    loop.create_task(coro)