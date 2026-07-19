# Task API

A small CRUD API for managing a to-do list, built with **FastAPI** (Python). Tasks are stored in memory — data resets whenever the server restarts.

Built as part of the FlyRank Internship Backend Track, Week 2, Assignment A1.

## Features

- Full CRUD: create, read, update, and delete tasks
- Input validation with proper status codes
- Interactive API docs via Swagger UI at `/docs`

## Requirements

- Python 3.10+

## How to run

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be running at `http://localhost:8000`.

## Endpoints

| Method | Path            | Description                          |
|--------|-----------------|---------------------------------------|
| GET    | `/`             | API info                             |
| GET    | `/health`       | Health check                         |
| GET    | `/tasks`        | List all tasks                       |
| GET    | `/tasks/{id}`   | Get a single task by id              |
| POST   | `/tasks`        | Create a new task                    |
| PUT    | `/tasks/{id}`   | Update a task's title and/or done    |
| DELETE | `/tasks/{id}`   | Delete a task                        |

## Example request

```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
```

```
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

Interactive docs are available at `http://localhost:8000/docs`, where you can try out every endpoint directly in the browser.

![Swagger UI showing GET /tasks](swagger-screenshot.png)

## Note on in-memory storage

This API keeps all data in a Python list — nothing is saved to disk. Restarting the server resets the task list back to its original 3 example tasks. This is intentional for this stage of the assignment; persistent storage (a database) comes in Week 3.
