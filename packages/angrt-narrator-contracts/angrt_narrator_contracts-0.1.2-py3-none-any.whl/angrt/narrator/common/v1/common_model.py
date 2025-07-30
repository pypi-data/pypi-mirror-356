# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1 
# Pydantic Version: 2.11.7 
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import Field
import typing


class SlotDefinition(BaseModel):
    name: str = Field(default="")
    type: str = Field(default="")
    required: bool = Field(default=False)
    description: str = Field(default="")
    is_entity_ref: bool = Field(default=False)
    entity_type: str = Field(default="")
    default_value: str = Field(default="")

class Template(BaseModel):
    id: str = Field(default="")
    name: str = Field(default="")
    title: str = Field(default="")
    description: str = Field(default="")
    category: str = Field(default="")
    keywords: typing.List[str] = Field(default_factory=list)
    slots: typing.List[SlotDefinition] = Field(default_factory=list)
