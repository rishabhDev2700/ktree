'''This file contains models of nodes and bits'''
from typing import List, Optional
from pydantic import BaseModel, Field

from models.database import PyObjectId


class BitModel(BaseModel):
    '''Bit model for validating bits'''
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(...)
    description: str = Field(...)
    url: str = Field(...)


class NodeModel(BaseModel):
    '''Node model for validating node data'''
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    owner: Optional[PyObjectId] = Field(alias="owner")
    name: str = Field(...)
    description: str = Field(...)
    related_nodes: List[PyObjectId]
    bits:List[BitModel]


class NodeCollection(BaseModel):
    '''Model for returning a list of nodes'''
    nodes:List[NodeModel]
    