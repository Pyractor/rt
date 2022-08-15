import traceback
import hashlib
from typing import List, Optional
from pydantic import BaseModel

class Slider(BaseModel):
    id: str
    value: Optional[int] = None
    max: int = 0
    min: int = 100

class Markdown(BaseModel):
    id: str
    md: str = ""

global __REGISTRY
__REGISTRY = dict()

def reset():
    __REGISTRY = dict()

def register(id, obj):
    __REGISTRY[id] = obj

def get(id, default):
    return __REGISTRY.get(id, default)

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
