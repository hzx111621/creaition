from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.services.ai_service import get_ai_service
from src.services.task_service import task_service

router = APIRouter(prefix="/ai", tags=["AI"])

class ParseTaskRequest(BaseModel):
    text: str

class SuggestTagsRequest(BaseModel):
    title: str
    description: str = ""

class SuggestPriorityRequest(BaseModel):
    title: str
    description: str = ""

class BreakdownTaskRequest(BaseModel):
    title: str
    description: str = ""

class SummarizeTasksRequest(BaseModel):
    pass

@router.post("/parse-task")
def parse_task(req: ParseTaskRequest):
    try:
        ai = get_ai_service()
        result = ai.parse_task_from_natural_language(req.text)
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.post("/suggest-tags")
def suggest_tags(req: SuggestTagsRequest):
    try:
        ai = get_ai_service()
        tags = ai.suggest_tags(req.title, req.description)
        return {"tags": tags}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.post("/suggest-priority")
def suggest_priority(req: SuggestPriorityRequest):
    try:
        ai = get_ai_service()
        priority = ai.suggest_priority(req.title, req.description)
        return {"priority": priority}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.post("/breakdown-task")
def breakdown_task(req: BreakdownTaskRequest):
    try:
        ai = get_ai_service()
        subtasks = ai.breakdown_task(req.title, req.description)
        return {"subtasks": subtasks}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.post("/summarize-tasks")
def summarize_tasks(req: SummarizeTasksRequest):
    try:
        ai = get_ai_service()
        tasks = task_service.get_all()
        task_dicts = [
            {
                "title": t.title,
                "description": t.description or "",
                "status": t.status.value,
                "priority": t.priority.value,
                "tags": t.tags,
                "due_date": t.due_date,
            }
            for t in tasks
        ]
        summary = ai.summarize_tasks(task_dicts)
        return {"summary": summary, "total_tasks": len(task_dicts)}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
