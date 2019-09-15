#!/usr/bin/env python

# WS server example

import asyncio
import websockets

async def hello(websocket, path):
    # wait websocket.send(f"> Welcome to Websocket")
    while True:
        name = await websocket.recv()
        
        if name=="quit":
            print(f"Client disconnected.")
        else :
            print(f"< {name}")

            greeting = f"Hello {name}!"

            await websocket.send(greeting)
            print(f"> {greeting}")

start_server = websockets.serve(hello, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()