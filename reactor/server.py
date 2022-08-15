import asyncio
import websockets
import json
from typing import List, Optional, Union, Any
from pydantic import BaseModel

class Hello(BaseModel):
    session: str

class Change(BaseModel):
    id: str
    value: Any

class StateSync(BaseModel):
    state: Any

class MessageIn(BaseModel):
    kind: str
    message: Union[Hello, Change]

class MessageOut(BaseModel):
    kind: str
    message: Union[StateSync, Hello]

async def echo(websocket):
    async for message in websocket:
        msg = MessageIn.parse_raw(message)
        print(message)
        print(msg)
        if msg.kind == "Hello":
            await websocket.send(StateSync(state="bebebe").json())

async def main():
    host = "localhost"
    port = 1337
    print(f"Running on {host}:{port}")
    async with websockets.serve(echo, host, port):
        await asyncio.Future()


def start():
    asyncio.run(main())
