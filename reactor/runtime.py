import traceback
import hashlib
from typing import List, Optional, Dict, Any, Callable
from pydantic import BaseModel

class Slider(BaseModel):
    id: str
    kind: str = "Slider"
    visible: bool = True
    value: Optional[int] = None
    max: int = 0
    min: int = 100

class Markdown(BaseModel):
    id: str
    kind: str = "MD"
    visible: bool = True
    md: str = ""

class Button(BaseModel):
    id: str
    kind: str = "Button"
    visible: bool = True
    label: str = ""

class Checkbox(BaseModel):
    id: str
    kind: str = "Checkbox"
    visible: bool = True
    value: bool = False
    label: str = ""

class Image(BaseModel):
    id: str
    kind: str = "Image"
    visible: bool = True
    src: str = ""

global __CALLBACKS
global __REGISTRY
global __ORDER
__CALLBACKS: Dict[str, Callable] = dict()
__REGISTRY: Dict[str, Any] = dict()
__ORDER: List[str] = list()

def reset_callbacks():
    __CALLBACKS = dict()

def reset_registry():
    __REGISTRY = dict()

def reset_order():
    __ORDER = list()

def reset():
    reset_callbacks()
    reset_registry()
    reset_order()

def register(id, obj, cb: Optional[Callable] = None):
    __REGISTRY[id] = obj
    if cb != None and callable(cb):
        __CALLBACKS[id] = cb
    if id not in __ORDER:
        __ORDER.append(id)

def get(id, default):
    return __REGISTRY.get(id, default)

def change(id: str, value: int):
    if id in __REGISTRY:
        if hasattr(__REGISTRY[id], 'value'):
            __REGISTRY[id].value = value
        if id in __CALLBACKS:
            __CALLBACKS[id]()


def call_id():
    stack = traceback.format_stack()
    fmt = "|".join(map(lambda s: s.strip(), stack))
    sha = hashlib.sha256(fmt.encode('ascii')).hexdigest()
    return sha

def slider(default = 50, min = 0, max = 100, visible = True, on_change: Optional[Callable] = None):
    id = call_id()
    obj = get(id, Slider(id=id))
    if obj.value == None:
        obj.value = default
    obj.min = min
    obj.max = max
    obj.visible = visible
    register(id, obj, on_change)
    return obj

def md(md = "", visible = True):
    id = call_id()
    obj = get(id, Markdown(id=id))
    obj.md = md
    obj.visible = visible
    register(id, obj)
    return obj

def button(label = "Button",  visible = True, on_click: Optional[Callable] = None):
    id = call_id()
    obj = get(id, Button(id=id))
    obj.label = label
    obj.visible = visible
    register(id, obj, on_click)
    return obj

def img(src = "", visible = True, on_click: Optional[Callable] = None):
    id = call_id()
    obj = get(id, Image(id=id))
    obj.src = src
    obj.visible = visible
    register(id, obj, on_click)
    return obj

def checkbox(default = False, label = "Checkbox", visible = True, on_change: Optional[Callable] = None):
    id = call_id()
    obj = get(id, Checkbox(id=id, value=default))
    obj.label = label
    obj.visible = visible
    register(id, obj)
    return obj
