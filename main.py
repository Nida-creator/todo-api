from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Walk the dog", "done": True},
    {"id": 3, "title": "Finish assignment", "done": False},
]

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body — title is required"},
    )

@app.get("/", summary="API info")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health", summary="Health check")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", summary="List all tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", summary="Get one task")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")

    next_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": next_id, "title": task.title, "done": False}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, task: TaskUpdate):
    if task.title is not None and not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    for t in tasks:
        if t["id"] == task_id:
            if task.title is not None:
                t["title"] = task.title
            if task.done is not None:
                t["done"] = task.done
            return t

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks.pop(i)
            return

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")