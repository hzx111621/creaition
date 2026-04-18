from typing import List, Optional
from datetime import datetime

from src.database import get_db
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate, TaskStatus, TaskPriority

class TaskService:
    def create(self, data: TaskCreate) -> Task:
        task = Task.create_new(
            title=data.title,
            description=data.description,
            status=TaskStatus(data.status.value) if data.status else TaskStatus.PENDING,
            priority=TaskPriority(data.priority.value) if data.priority else TaskPriority.MEDIUM,
            tags=data.tags,
            due_date=data.due_date,
        )
        with get_db() as conn:
            conn.execute(
                "INSERT INTO tasks (id, title, description, status, priority, tags, created_at, updated_at) "
                "VALUES (:id, :title, :description, :status, :priority, :tags, :created_at, :updated_at)",
                task.to_row(),
            )
            conn.commit()
        return task

    def get_by_id(self, task_id: str) -> Optional[Task]:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if row:
                return Task.from_row(row)
            return None

    def get_all(self, status: Optional[str] = None, priority: Optional[str] = None,
                tag: Optional[str] = None) -> List[Task]:
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        if tag:
            query += " AND tags LIKE ?"
            params.append(f"%{tag}%")
        query += " ORDER BY created_at DESC"
        with get_db() as conn:
            rows = conn.execute(query, params).fetchall()
            return [Task.from_row(row) for row in rows]

    def update(self, task_id: str, data: TaskUpdate) -> Optional[Task]:
        task = self.get_by_id(task_id)
        if not task:
            return None

        updated_values = {}
        if data.title is not None:
            updated_values["title"] = data.title
        if data.description is not None:
            updated_values["description"] = data.description
        if data.status is not None:
            updated_values["status"] = data.status.value
        if data.priority is not None:
            updated_values["priority"] = data.priority.value
        if data.tags is not None:
            updated_values["tags"] = __import__("json").dumps(data.tags, ensure_ascii=False)
        if data.due_date is not None:
            updated_values["due_date"] = data.due_date

        if not updated_values:
            return task

        updated_values["updated_at"] = datetime.utcnow().isoformat()
        set_clause = ", ".join(f"{k} = ?" for k in updated_values)
        values = list(updated_values.values()) + [task_id]

        with get_db() as conn:
            conn.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
            conn.commit()

        return self.get_by_id(task_id)

    def delete(self, task_id: str) -> bool:
        with get_db() as conn:
            cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return cur.rowcount > 0

task_service = TaskService()
