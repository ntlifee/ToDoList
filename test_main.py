import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from bson.objectid import ObjectId
from schemas_task import tasks_entity, task_entity
from main import app

client = TestClient(app)


@pytest.fixture
def mock_mongodb_connection():
    with patch("main.MongoDBConnection") as mock_mongodb:
        # Настраиваем фейковое подключение
        mock_connection = mock_mongodb.return_value.__enter__.return_value
        yield mock_connection


def test_find_tasks_success(mock_mongodb_connection):
    value = {"_id": ObjectId(), "title": "Test Task",
             "description": "Test Description", "completed": False}

    mock_mongodb_connection.todo.tasks.find.return_value = [value]

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == tasks_entity([value])


def test_find_tasks_empty_list(mock_mongodb_connection):
    mock_mongodb_connection.todo.tasks.find.return_value = []

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == []


def test_add_task_success(mock_mongodb_connection):
    task_data = {"title": "New Task",
                 "description": "New Description", "completed": False}
    inserted_id = ObjectId()
    inserted_task = {"_id": inserted_id, **task_data}

    mock_mongodb_connection.todo.tasks.find_one.return_value = inserted_task

    response = client.post("/", json=task_data)

    assert response.status_code == 201
    assert response.json() == {
        "message": "Task added successfully",
        "task": task_entity(inserted_task)
    }
