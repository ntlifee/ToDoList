def task_entity(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "completed": task["completed"]
    }


def tasks_entity(tasks) -> list[dict]:
    return [task_entity(task) for task in tasks]
