from dataclasses import dataclass
from bs4.element import Tag
from typing import Optional, Self
from enum import Enum

class InputType(Enum):
    BUTTON = "button"
    CHECKBOX = "checkbox"
    COLOR = "color"
    DATE = "date"
    DATETIMELOCAL = "datetime-local"
    EMAIL = "email"
    FILE = "file"
    HIDDEN = "hidden"
    IMAGE = "image"
    MONTH = "month"
    NUMBER = "number"
    PASSWORD = "password"
    RADIO = "radio"
    RANGE = "range"
    RESET = "reset"
    SEARCH = "search"
    SUBMIT = "submit"
    TEL = "tel"
    TEXT = "text"
    TIME = "time"
    URL = "url"
    WEEK = "week"
    
    @classmethod
    def from_str(cls, s: str) -> Self:
        for input_type in cls:
            if input_type.value == s:
                return input_type
        
        raise Exception(f"InputType \"{s}\" not known...")
    
class Method(Enum):
    GET = "get"
    POST = "post"
    NONE = "none"
    
    @classmethod
    def from_str(cls, s: str) -> Self:
        for method in cls:
            if method.value == s.lower():
                return method
        
        raise Exception(f"Method \"{s}\" not known...")
            
    
@dataclass
class Form:
    id_: Optional[str] = None
    action: Optional[str] = None
    type_: Optional[str] = None
    method: Method = Method.NONE
    meta_id: int = -1
    
    @classmethod
    def from_tag(cls, tag: Tag, meta_id: int) -> Self:
        return cls(
            action=tag.get("action", None),
            method=Method.from_str(tag.get("method", "none")),
            type_=tag.get("type", None),
            meta_id=meta_id,
        )
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}<({self.meta_id}), id:{self.id_}, action:{self.action}, method:{self.method}, type:{self.type_}>"
    
@dataclass
class Input:
    id_: Optional[str] = None
    name: Optional[str] = None
    placeholder: Optional[str] = None
    type_: InputType = InputType.TEXT
    meta_id: int = -1
    
    @classmethod
    def from_tag(cls, tag: Tag, meta_id: int) -> Self:
        return cls(
            id_=tag.get("id", None),
            name=tag.get("name", None),
            placeholder=tag.get("placeholder", None),
            type_=InputType.from_str(tag.get("type", None)),
            meta_id=meta_id,
        )
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}<({self.meta_id}), id:{self.id_}, type:{self.type_.value}, name:{self.name}, placeholder:{self.placeholder}>"
