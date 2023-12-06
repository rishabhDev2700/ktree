from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException
from models.database import db
from models.node import BitModel, NodeCollection, NodeModel
from models.schema import DeleteBitModel


router = APIRouter(prefix="/nodes")


@router.get("/", response_model=NodeCollection)
async def get_all_nodes():
    '''
    Get all nodes of a user
    '''
    return NodeCollection(nodes=await db["nodes"].find({}).to_list(1000))


@router.post("/{id}/add", response_model=BitModel)
async def add_bit_to_node(id: str, bit: BitModel = Body(...)):
    '''
    Method to add a new bit to the specified node
    '''
    node: NodeModel = await db["nodes"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$push": {"bits": bit}}
    )
    if node is not None:
        return node
    else:
        return HTTPException(status_code=404, detail="Node not found")


@router.post("/bit/delete", response_model=NodeModel)
async def delete_bit(bit: DeleteBitModel = Body(...)):
    '''
    Method to delete a specific bit from the specified node
    '''
    result = await db["nodes"].update_one(
        {"_id": ObjectId(bit.node_id)}, {"$pull": {"_id": ObjectId(bit.bit_id)}}
    )
    if result is None:
        return result
    else:
        return HTTPException(status_code=204,detail="Some error occurred!")
    return NodeModel
