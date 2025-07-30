# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field

from .common_p2p import Template


class GetTemplateRequest(BaseModel):
    """
    ---------- RPC-обёртки ----------
    """

    template_id: str = Field(default="")


class GetTemplateResponse(BaseModel):
    template: Template = Field(default_factory=Template)


class FindTemplatesRequest(BaseModel):
    query: str = Field(default="")
    category: str = Field(default="")
    top_k: int = Field(default=0)


class FindTemplatesResponse(BaseModel):
    templates: typing.List[Template] = Field(default_factory=list)


class UpsertTemplateRequest(BaseModel):
    template: Template = Field(default_factory=Template)


class UpsertTemplateResponse(BaseModel):
    template: Template = Field(default_factory=Template)
