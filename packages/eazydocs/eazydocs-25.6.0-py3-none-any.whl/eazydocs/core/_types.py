from pathlib import Path
from types import FunctionType, MethodType
from typing import NamedTuple, TypedDict, Union


class ParamsDict(TypedDict):
    arg_type: str
    description: str
    default_value: str


class ArgsTuple(NamedTuple):
    param: str
    arg_type: str
    description: str


FunctionMethodType = Union[FunctionType, MethodType]
ClassMethodType = Union[object, FunctionMethodType]
StrPathType = Union[str, Path]
