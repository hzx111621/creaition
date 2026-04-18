from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
import json
import uuid

from src.schemas.task import TaskStatus, TaskPriority

@dataclass
class Task:
    id: str
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    tags: List[str]
    due_date: Optional[str]
    created_at: str
    updated_at: str

    @classmethod
    def from_row(cls, row) -> "Task":
        tags_raw = row["tags"]
        tags = json.loads(tags_raw) if tags_raw else []
        return cls(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            status=TaskStatus(row["status"]),
            priority=TaskPriority(row["priority"]),
            tags=tags,
            due_date=row["due_date"] if "due_date" in row.keys() else None,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @classmethod
    def create_new(cls, title: str, description: Optional[str] = None,
                   status: TaskStatus = TaskStatus.PENDING,
                   priority: TaskPriority = TaskPriority.MEDIUM,
                   tags: Optional[List[str]] = None,
                   due_date: Optional[str] = None) -> "Task":
        now = datetime.utcnow().isoformat()
        return cls(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            status=status,
            priority=priority,
            tags=tags or [],
            due_date=due_date,
            created_at=now,
            updated_at=now,
        )

    def to_row(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "tags": json.dumps(self.tags, ensure_ascii=False),
            "due_date": self.due_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
