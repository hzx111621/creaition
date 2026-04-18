"""Integration tests for task API endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


class TestHealthEndpoint:
    @pytest.mark.asyncio
    async def test_health_check(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestTaskEndpoints:
    @pytest.mark.asyncio
    async def test_create_task(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/tasks", json={
                "title": "Test task",
                "description": "Test description",
                "priority": "high",
                "tags": ["test"]
            })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test task"
        assert data["description"] == "Test description"
        assert data["priority"] == "high"
        assert data["tags"] == ["test"]
        assert data["status"] == "pending"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    @pytest.mark.asyncio
    async def test_create_task_minimal(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/tasks", json={"title": "Minimal task"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal task"
        assert data["status"] == "pending"
        assert data["priority"] == "medium"

    @pytest.mark.asyncio
    async def test_get_task_not_found(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/tasks/nonexistent-id")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_tasks_empty(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_list_tasks_with_data(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            await client.post("/tasks", json={"title": "Task 1"})
            await client.post("/tasks", json={"title": "Task 2"})
            response = await client.get("/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    @pytest.mark.asyncio
    async def test_get_task_by_id(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_resp = await client.post("/tasks", json={"title": "Get me"})
            task_id = create_resp.json()["id"]
            response = await client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Get me"

    @pytest.mark.asyncio
    async def test_update_task(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_resp = await client.post("/tasks", json={"title": "Original"})
            task_id = create_resp.json()["id"]
            response = await client.put(f"/tasks/{task_id}", json={
                "title": "Updated",
                "status": "completed"
            })
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"
        assert data["status"] == "completed"

    @pytest.mark.asyncio
    async def test_update_task_partial(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_resp = await client.post("/tasks", json={
                "title": "Partial",
                "priority": "low"
            })
            task_id = create_resp.json()["id"]
            response = await client.put(f"/tasks/{task_id}", json={
                "status": "in_progress"
            })
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Partial"
        assert data["status"] == "in_progress"
        assert data["priority"] == "low"

    @pytest.mark.asyncio
    async def test_update_task_not_found(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.put("/tasks/nonexistent-id", json={
                "title": "Updated"
            })
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_task(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_resp = await client.post("/tasks", json={"title": "Delete me"})
            task_id = create_resp.json()["id"]
            response = await client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete("/tasks/nonexistent-id")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_filter_tasks_by_status(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            await client.post("/tasks", json={"title": "Pending task"})
            completed = await client.post("/tasks", json={
                "title": "Completed task",
                "status": "completed"
            })
            completed_id = completed.json()["id"]
            await client.put(f"/tasks/{completed_id}", json={"status": "completed"})
            response = await client.get("/tasks?status=completed")
        data = response.json()
        assert all(t["status"] == "completed" for t in data)

    @pytest.mark.asyncio
    async def test_filter_tasks_by_priority(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            await client.post("/tasks", json={"title": "Low priority", "priority": "low"})
            await client.post("/tasks", json={"title": "High priority", "priority": "high"})
            response = await client.get("/tasks?priority=high")
        data = response.json()
        assert all(t["priority"] == "high" for t in data)

    @pytest.mark.asyncio
    async def test_filter_tasks_by_tag(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            await client.post("/tasks", json={"title": "Work task", "tags": ["work"]})
            await client.post("/tasks", json={"title": "Home task", "tags": ["home"]})
            response = await client.get("/tasks?tag=work")
        data = response.json()
        assert all("work" in t["tags"] for t in data)

    @pytest.mark.asyncio
    async def test_create_task_with_due_date(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/tasks", json={
                "title": "Task with deadline",
                "due_date": "2026-04-25"
            })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Task with deadline"
        assert data["due_date"] == "2026-04-25"

    @pytest.mark.asyncio
    async def test_update_task_with_due_date(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_resp = await client.post("/tasks", json={"title": "Update date"})
            task_id = create_resp.json()["id"]
            response = await client.put(f"/tasks/{task_id}", json={
                "due_date": "2026-05-01"
            })
        assert response.status_code == 200
        assert response.json()["due_date"] == "2026-05-01"

    @pytest.mark.asyncio
    async def test_create_task_invalid_title(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/tasks", json={"title": ""})
        assert response.status_code == 422
