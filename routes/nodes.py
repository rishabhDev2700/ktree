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

@router.post('/node/add',response_model=NodeCollection)
async def add_node(new_node: NodeModel=Body(...)):
    '''
    Method to add a new node 
    '''
    node = await db['nodes'].insert_one(new_node.model_dump(by_alias=True, exclude={'id'}))
    nodes = await db['nodes'].find({"username":"username"}).to_list(1000)
    return NodeCollection(nodes=nodes)

@router.post("/{id}/add", response_model=BitModel)
async def add_bit_to_node(id: str, bit: BitModel = Body(...)):
    '''
    Method to add a new bit to the specified node
    '''
    node: NodeModel = await db["nodes"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$push": {"bits": bit.model_dump(by_alias=True)}}
    )
    if node is not None:
        return node
    else:
        return HTTPException(status_code=404, detail="Node not found")


@router.post("/bit/delete")
async def delete_bit(bit: DeleteBitModel = Body(...)):
    '''
    Method to delete a specific bit from the specified node
    '''
    result = await db["nodes"].update_one(
        {"_id": ObjectId(bit.node_id)}, {"$pull": {"_id": ObjectId(bit.bit_id)}}
    )
    if result is None:
        return {"status":200, "message":"Bit deleted successfully"}
    else:
        return HTTPException(status_code=204,detail="Some error occurred!")