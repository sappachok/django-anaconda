#!/usr/bin/env python

# WS client example

import asyncio
import websockets

async def hello():
    uri = "ws://127.0.0.1:5678"
    async with websockets.connect(uri) as websocket:
        while True:
            name = input("What's your name? ")

            if name == "quit":
                print(f"> {name}")
                break
                
            await websocket.send(name)
            print(f"> {name}")

            greeting = await websocket.recv()
            print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())