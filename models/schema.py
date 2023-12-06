from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_core import Url

from models.database import PyObjectId
from models.node import BitModel

class DeleteBitModel(BaseModel):
    node_id: Optional[str] = None
    bit_id: Optional[str] = None

class UpdateBitModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    url: Optional[str]

class UpdateNodeModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    parent: Optional[PyObjectId]

class DeleteNodeModel(BaseModel):
    node_id:str