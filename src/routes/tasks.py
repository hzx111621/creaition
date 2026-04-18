from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from src.services.task_service import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=TaskResponse, status_code=201)
def create_task(data: TaskCreate):
    task = task_service.create(data)
    return TaskResponse(**vars(task))

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    task = task_service.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(**vars(task))

@router.get("", response_model=list[TaskResponse])
def list_tasks(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
):
    tasks = task_service.get_all(status=status, priority=priority, tag=tag)
    return [TaskResponse(**vars(t)) for t in tasks]

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, data: TaskUpdate):
    task = task_service.update(task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(**vars(task))

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: str):
    deleted = task_service.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
