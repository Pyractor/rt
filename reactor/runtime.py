import traceback
import hashlib
from typing import List, Optional, Dict, Any
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

global __REGISTRY
global __ORDER
__REGISTRY: Dict[str, Any] = dict()
__ORDER: List[str] = list()

def reset_registry():
    __REGISTRY = dict()

def reset_order():
    __ORDER = list()

def reset():
    reset_registry()
    reset_order()

def register(id, obj):
    __REGISTRY[id] = obj
    if id not in __ORDER:
        __ORDER.append(id)

def get(id, default):
    return __REGISTRY.get(id, default)

def change(id: str, value: int):
    if id in __REGISTRY:
        __REGISTRY[id].value = value

def call_id():
    stack = traceback.format_stack()
    fmt = "|".join(map(lambda s: s.strip(), stack))
    sha = hashlib.sha256(fmt.encode('ascii')).hexdigest()
    return sha

def slider(default = 50, min = 0, max = 100):
    id = call_id()
    obj = get(id, Slider(id=id))
    obj.value = obj.value or default
    obj.min = min
    obj.max = max
    register(id, obj)
    return obj

def md(md = ""):
    id = call_id()
    obj = get(id, Markdown(id=id))
    obj.md = md
    register(id, obj)
    return obj
