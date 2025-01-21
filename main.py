from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, RedirectResponse
from pymongo import MongoClient
from bson.objectid import ObjectId
import env

app = FastAPI()

client = MongoClient(env.DATABASE)
db = client["todo_db"]
tasks_collection = db["tasks"]


@app.get('/')
async def todo(title=None, description=None) -> JSONResponse:
    query = {}
    if title is not None:
        query["title"] = {"$regex": title}
    if description is not None:
        query["description"] = {"$regex": description}

    tasks = []
    for task in tasks_collection.find(query):
        task["_id"] = str(task["_id"])
        tasks.append(task)
    return JSONResponse(tasks, status_code=200)


@app.post('/addToDo')
async def add_todo(to_do: dict = Body()) -> RedirectResponse:
    tasks_collection.insert_one(to_do)
    return JSONResponse({"message": "Task added successfully"},
                        status_code=200)


@app.delete('/{id_to_do}')
async def delete(id_to_do: str):
    tasks_collection.delete_one({"_id": ObjectId(id_to_do)})
    return JSONResponse({"message": "Task deleted successfully"},
                        status_code=200)


@app.put('/{id_to_do}')
async def update(id_to_do: str, updated_task: dict = Body()) -> JSONResponse:
    tasks_collection.update_one({"_id": ObjectId(id_to_do)},
                                {"$set": updated_task})
    return JSONResponse({"message": "Task updated successfully"},
                        status_code=200)
