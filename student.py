# Authores

# Name:  Edgar Sousa                          NMEC:   98757
# Name:  João Castanheira                     NMEC:   97521


from engine import Engine
import threading
import websockets
import os
import asyncio
import getpass
import json

# websocket info
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())

# input and output messages
IN_QUEUE = list()
OUT_QUEUE = list()

# mutexes for threading
IN_QUEUE_LOCK = threading.Condition(threading.Lock())
OUT_QUEUE_LOCK = threading.Condition(threading.Lock())

def state_handler():
    last_state = ''
    while True:
        try:
            IN_QUEUE_LOCK.acquire()
            IN_QUEUE_LOCK.wait()
            state = IN_QUEUE.pop(0)
            IN_QUEUE_LOCK.release()

            if str(state['game']) == last_state:
                continue

            if state['piece'] == None:
                continue

            last_state = str(state['game'])         

            game = Engine.from_json(state)

            next_states = game.calc_states()

            next_states.sort()

            OUT_QUEUE_LOCK.acquire()
            OUT_QUEUE.extend(next_states[0].plays[-1])
            OUT_QUEUE_LOCK.release()

        except Exception as e:
            print(e)


async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        # skip 1st message
        await websocket.recv()

        while True:
            try:
                # get json from server
                state = json.loads(
                    await websocket.recv()
                )

                # put json into in queue
                IN_QUEUE_LOCK.acquire()
                IN_QUEUE.append(state)
                IN_QUEUE_LOCK.notify()
                IN_QUEUE_LOCK.release()

                # get keypress from out queue
                key = ''
                OUT_QUEUE_LOCK.acquire()
                if OUT_QUEUE:
                    key = OUT_QUEUE.pop(0)
                OUT_QUEUE_LOCK.release()

                # send keypress to server
                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )

            except Exception as e:
                print(e)
                return

def main():
    threading.Thread(target=state_handler).start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))

if __name__ == '__main__':
    main()