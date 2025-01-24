from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from model_task import Task
from db import MongoDBConnection
from schemas_task import tasks_entity, task_entity

app = FastAPI()


@app.get("/")
async def find_tasks() -> JSONResponse:
    with MongoDBConnection() as connection:
        tasks_collection = connection.todo.tasks
        tasks = tasks_entity(tasks_collection.find())
        return JSONResponse(tasks, status_code=200)


@app.post("/")
async def add_task(task: Task) -> JSONResponse:
    with MongoDBConnection() as connection:
        tasks_collection = connection.todo.tasks
        insert_result = tasks_collection.insert_one(dict(task))
        insert_task = task_entity(tasks_collection.find_one(
            {"_id": insert_result.inserted_id}))
        return JSONResponse({"message": "Task added successfully",
                             "task": insert_task},
                            status_code=201)


@app.delete("/{task_id}")
async def delete_task(task_id: str) -> JSONResponse:
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    with MongoDBConnection() as connection:
        tasks_collection = connection.todo.tasks
        delete_result = tasks_collection.delete_one({"_id": ObjectId(task_id)})

        if delete_result.deleted_count == 1:
            return JSONResponse({"message": "Task deleted successfully"},
                                status_code=200)
        raise HTTPException(status_code=404, detail="Task not found")


@app.put("/{task_id}")
async def update_task(task_id: str, task: Task) -> JSONResponse:
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    with MongoDBConnection() as connection:
        tasks_collection = connection.todo.tasks

        existing_task = tasks_collection.find_one({"_id": ObjectId(task_id)})
        if not existing_task:
            raise HTTPException(status_code=404, detail="Task not found")

        update_result = tasks_collection.update_one({"_id": ObjectId(task_id)},
                                                    {"$set": dict(task)})
        if update_result.modified_count == 1:
            updated_task = task_entity(tasks_collection.find_one(
                {"_id": ObjectId(task_id)}))
            return JSONResponse({"message": "Task updated successfully",
                                 "task": updated_task},
                                status_code=200)
        raise HTTPException(status_code=400, detail="Update failed")
