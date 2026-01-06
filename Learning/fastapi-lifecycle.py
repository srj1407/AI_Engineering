from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import time
import asyncio

app = FastAPI()

class TaskRequest(BaseModel):
    task_name: str
    duration: int

def run_task(task_name, duration):
    print(f'Start {task_name}')
    time.sleep(duration)
    print(f'Task ended.')

# async def run_task(task_name, duration):
#     print(f'Start {task_name}')
#     time.sleep(duration)
#     print(f'Task ended.')

# async def run_task(task_name, duration):
#     print(f'Start {task_name}')
#     await asyncio.sleep(duration)
#     print(f'Task ended.')

@app.post("/tasks")
async def create_task(taskRequest: TaskRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_task, taskRequest.task_name, taskRequest.duration)
    return { "message": "task accepted" }

@app.get("/health")
async def get_health():
    return { "message": "Running health" }
