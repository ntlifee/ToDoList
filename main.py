from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from bson.objectid import ObjectId
from schemas_task import tasks_entity
from model_task import Task

app = FastAPI()

connection = MongoClient()
db = connection["todo"]
tasks_collection = db["tasks"]


@app.get('/')
async def find_tasks(title: str = None, description: str = None, completed: bool = None) -> JSONResponse:
    query = {}
    if title is not None:
        query["title"] = {"$regex": title}
    if description is not None:
        query["description"] = {"$regex": description}
    if completed is not None:
        query["completed"] = completed
    return JSONResponse(tasks_entity(tasks_collection.find(query)),
                        status_code=200)


@app.post('/')
async def add_task(task: Task) -> JSONResponse:
    tasks_collection.insert_one(dict(task))
    return JSONResponse({"message": "Task added successfully"},
                        status_code=200)


@app.delete('/{id_task}')
async def delete_task(id_task: str) -> JSONResponse:
    tasks_collection.delete_one({"_id": ObjectId(id_task)})
    return JSONResponse({"message": "Task deleted successfully"},
                        status_code=200)


@app.put('/{id_task}')
async def update_task(id_task: str, task: Task) -> JSONResponse:
    tasks_collection.update_one({"_id": ObjectId(id_task)},
                                {"$set": dict(task)})
    return JSONResponse({"message": "Task updated successfully"},
                        status_code=200)
