from typing import Optional
from pydantic import BaseModel


class DeleteBitModel(BaseModel):
    """Model for deleting a bit"""
    node_id: str
    bit_id: str


class UpdateBitModel(BaseModel):
    """Model for deleting a bit"""
    title: Optional[str]
    description: Optional[str]
    url: Optional[str]


class UpdateNodeModel(BaseModel):
    """Model for deleting a bit"""
    name: Optional[str]
    description: Optional[str]


class DeleteNodeModel(BaseModel):
    """Model for deleting a bit"""
    node_id: str
