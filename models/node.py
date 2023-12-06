from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic_core import Url

from models.database import PyObjectId


class BitModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(...)
    description: str = Field(...)
    url: str = Field(...)


class NodeModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    description: str = Field(...)
    parent: Optional[PyObjectId] = Field(default=None)
    bits:List[BitModel] = []


class NodeCollection(BaseModel):
    nodes:List[NodeModel]