from dataclasses import dataclass
from bs4.element import Tag
from typing import Self
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
    
    def from_str(s: str) -> Self:
        for input_type in InputType:
            if input_type.value == s:
                return input_type
        
        raise Exception(f"InputType \"{s}\" not known...")
    
class Method(Enum):
    GET = "get"
    POST = "post"
    NONE = "none"
    
    def from_str(s: str) -> Self:
        for method in Method:
            if method.value == s.lower():
                return method
        
        raise Exception(f"Method \"{s}\" not known...")
            
    
@dataclass
class Form:
    action: str
    method: str
    type_: str
    
    @classmethod
    def from_tag(cls, tag: Tag) -> Self:
        return cls(
            action=tag.get("action", None),
            method=Method.from_str(tag.get("method", "none")),
            type_=tag.get("type", None),
        )
    
@dataclass
class Input:
    id_: str
    name: str
    placeholder: str
    type_: InputType
    
    @classmethod
    def from_tag(cls, tag: Tag) -> Self:
        return cls(
            id_=tag.get("id", None),
            name=tag.get("name", None),
            placeholder=tag.get("placeholder", None),
            type_=InputType.from_str(tag.get("type", None)),
        )
    
    def __str__(self) -> str:
        return f"{self.type_}<{self.id_}, {self.name_}, {self.placeholder}>"
