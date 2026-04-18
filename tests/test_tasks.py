"""Unit tests for task schemas and API endpoints."""
import pytest
from src.schemas.task import TaskCreate, TaskUpdate, TaskStatus, TaskPriority


class TestTaskSchemas:
    def test_task_create_schema(self):
        data = TaskCreate(
            title="Test task",
            description="A test description",
            priority=TaskPriority.HIGH,
            tags=["test"],
        )
        assert data.title == "Test task"
        assert data.description == "A test description"
        assert data.priority == TaskPriority.HIGH
        assert data.tags == ["test"]
        assert data.due_date is None

    def test_task_create_with_due_date(self):
        data = TaskCreate(
            title="Deadline task",
            due_date="2026-04-20",
        )
        assert data.title == "Deadline task"
        assert data.due_date == "2026-04-20"

    def test_task_create_minimal(self):
        data = TaskCreate(title="Minimal task")
        assert data.title == "Minimal task"
        assert data.description is None
        assert data.priority == TaskPriority.MEDIUM
        assert data.tags == []

    def test_task_create_with_all_fields(self):
        data = TaskCreate(
            title="Full task",
            description="All fields set",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.LOW,
            tags=["work", "urgent"],
            due_date="2026-05-01",
        )
        assert data.status == TaskStatus.IN_PROGRESS
        assert data.priority == TaskPriority.LOW
        assert len(data.tags) == 2
        assert data.due_date == "2026-05-01"

    def test_task_create_title_required(self):
        with pytest.raises(Exception):
            TaskCreate(title="")

    def test_task_update_partial(self):
        data = TaskUpdate(status=TaskStatus.COMPLETED)
        assert data.title is None
        assert data.description is None
        assert data.status == TaskStatus.COMPLETED
        assert data.priority is None
        assert data.tags is None
        assert data.due_date is None

    def test_task_update_multiple_fields(self):
        data = TaskUpdate(
            title="Updated title",
            priority=TaskPriority.HIGH,
            tags=["new-tag"],
            due_date="2026-04-25",
        )
        assert data.title == "Updated title"
        assert data.priority == TaskPriority.HIGH
        assert data.tags == ["new-tag"]
        assert data.due_date == "2026-04-25"

    def test_task_status_enum(self):
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.COMPLETED.value == "completed"

    def test_task_priority_enum(self):
        assert TaskPriority.LOW.value == "low"
        assert TaskPriority.MEDIUM.value == "medium"
        assert TaskPriority.HIGH.value == "high"
