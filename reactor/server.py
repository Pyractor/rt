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

class Loading(BaseModel):
    loading: bool = False

class StateSync(BaseModel):
    state: State

class MessageIn(BaseModel):
    kind: str
    message: Union[Hello, Change]

class MessageOut(BaseModel):
    kind: str
    message: Union[StateSync, Loading]

async def echo(websocket):
    async for message in websocket:
        msg = MessageIn.parse_raw(message)
        should_exec = False
        print(message)
        print(msg)

        if msg.kind == "Change" and isinstance(msg.message, Change):
            await websocket.send(MessageOut(kind="Loading", message=Loading(loading=True)).json())
            rt.change(msg.message.id, msg.message.value)
            should_exec = True

        if msg.kind == "Hello":
            rt.reset_order()
            should_exec = True

        if should_exec:
            await websocket.send(MessageOut(kind="Loading", message=Loading(loading=True)).json())
            exec(open("./main.py").read())
            msg = MessageOut(kind="StateSync", message=StateSync(state=State(registry=rt.__REGISTRY, order=rt.__ORDER)))
            await websocket.send(msg.json())

        await websocket.send(MessageOut(kind="Loading", message=Loading(loading=False)).json())

async def main():
    host = "localhost"
    port = 1337
    print(f"Running on {host}:{port}")
    async with websockets.serve(echo, host, port):
        await asyncio.Future()


def start():
    asyncio.run(main())
