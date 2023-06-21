import asyncio
import getpass
import json
import os
import random
from typing import AsyncGenerator, Tuple
from Student import agent
import time

import websockets

# Next 4 lines are not needed for AI agents, please remove them from your code!


 
async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        # Next 3 lines are not needed for AI agent

        while True:
            try:
                
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                print(state)
                # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                while True:     
                    key = agent(state)
                    await websocket.send(
                        json.dumps({"cmd": "key", "key": key})
                    )  # send key command to server - you must implement this send in the AI agent
                    break
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return



# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
