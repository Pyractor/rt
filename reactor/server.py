import asyncio
import websockets
import json
import reactor.runtime as rt
from typing import List, Optional, Union, Any, Dict
from pydantic import BaseModel

class Hello(BaseModel):
    session: str

class Change(BaseModel):
    id: str
    value: Any

class State(BaseModel):
    registry: Dict[str, Any]
    order: List[str]

class StateSync(BaseModel):
    state: State

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

        if msg.kind == "Change" and isinstance(msg.message, Change):
            rt.change(msg.message.id, msg.message.value)

        if msg.kind == "Hello":
            rt.reset_order()
            exec(open("./main.py").read())
            msg = MessageOut(kind="StateSync", message=StateSync(state=State(registry=rt.__REGISTRY, order=rt.__ORDER)))
            await websocket.send(msg.json())

async def main():
    host = "localhost"
    port = 1337
    print(f"Running on {host}:{port}")
    async with websockets.serve(echo, host, port):
        await asyncio.Future()


def start():
    asyncio.run(main())
