from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException

from models.database import db
from models.node import BitModel, NodeCollection, NodeModel
from models.schema import DeleteBitModel

router = APIRouter(prefix="/nodes")


@router.get("/{user_id}", response_model=NodeCollection)
async def get_all_nodes(user_id: str):
    """
    Get all nodes of a user
    """
    user = await db['users'].find_one({"_id": ObjectId(user_id)})
    nodes = await db['nodes'].find({"owner": ObjectId(user['_id'])}).to_list(100)
    return NodeCollection(nodes=nodes)


@router.post('/node/add', response_model=NodeModel)
async def add_node(new_node: NodeModel = Body(...)):
    """
    Method to add a new node
    """
    new_node.owner = ObjectId(new_node.owner)
    node = await db['nodes'].insert_one(new_node.model_dump(by_alias=True, exclude={'id'}))
    node = await db['nodes'].find_one({"_id": node.inserted_id})
    return node


@router.post("/{id}/add", response_model=NodeModel)
async def add_bit_to_node(id: str, bit: BitModel = Body(...)):
    """
    Method to add a new bit to the specified node
    """
    node: NodeModel = await db["nodes"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$push": {"bits": bit.model_dump(by_alias=True)}}
    )
    if node is not None:
        return node
    else:
        return HTTPException(status_code=404, detail="Node not found")


@router.post("/bit/delete")
async def delete_bit(bit: DeleteBitModel = Body(...)):
    """
    Method to delete a specific bit from the specified node
    """
    result = await db["nodes"].update_one(
        {"_id": ObjectId(bit.node_id)}, {"$pull": {"_id": ObjectId(bit.bit_id)}}
    )
    if result is None:
        return {"status": 200, "message": "Bit deleted successfully"}
    else:
        return HTTPException(status_code=204, detail="Some error occurred!")
