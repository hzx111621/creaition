# Intelligent Task Management System / 智能任务管理系统

> English below / 中文在下方

[![Tests](https://img.shields.io/badge/tests-27%20passed-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

---

## English

### Tech Stack
Python 3.10+ · FastAPI · SQLite · SiliconFlow API

### Features
- **Task Management** — Full CRUD via RESTful API, filter by status/priority/tags, SQLite persistence
- **AI Parsing** — Convert natural language ("明天下午3点提醒我开会") into structured tasks
- **Smart Suggestions** — AI recommends tags and priority based on task content
- **Task Breakdown** — Split complex tasks into 3-7 actionable subtasks
- **Task Summarization** — Generate overview of all current tasks
- **Web UI** — Browser-based testing panel, no build step required

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env: set SILICONFLOW_API_KEY and DEFAULT_MODEL

# Start backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
# API: http://localhost:8000
# Docs: http://localhost:8000/docs

# Open testing panel
# Double-click frontend/index.html
# Or serve it:
cd frontend && python -m http.server 8080
# Then visit http://localhost:8080
```

### API Reference

**Tasks**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks (`?status=`, `?priority=`, `?tag=` filters) |
| GET | `/tasks/{id}` | Get a single task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

**AI**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ai/parse-task` | Parse natural language into a task |
| POST | `/ai/suggest-tags` | Get tag suggestions |
| POST | `/ai/suggest-priority` | Get priority recommendation |
| POST | `/ai/breakdown-task` | Break a task into subtasks |
| POST | `/ai/summarize-tasks` | Summarize all tasks |

### Run Tests

```bash
pytest tests/ -v
```

### Project Structure

```
src/
  main.py           FastAPI entry point
  config.py         Configuration loader
  database.py       SQLite database setup
  models/task.py    Task data model
  schemas/task.py   Pydantic request/response schemas
  services/
    ai_service.py   SiliconFlow API client
    task_service.py Task business logic
  routes/
    tasks.py        Task CRUD endpoints
    ai.py           AI feature endpoints
frontend/
  index.html        Web testing panel (single file, no build required)
tests/
  conftest.py       pytest fixtures
  test_api.py       API integration tests
  test_tasks.py     Task service unit tests
```

### Notes
- AI features require a valid SiliconFlow API key. Get one free at [siliconflow.cn](https://siliconflow.cn).
- Default model is set via `DEFAULT_MODEL` in `.env`.
- The frontend is a standalone HTML file — no npm or build tools needed.

---

## 中文

[![Tests](https://img.shields.io/badge/tests-27%20passed-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

### 技术栈
Python 3.10+ · FastAPI · SQLite · SiliconFlow API

### 功能特性
- **任务管理** — RESTful API 完整增删改查，支持按状态/优先级/标签筛选，SQLite 持久化
- **AI 自然语言解析** — 将"明天下午3点提醒我开会"自动转换为结构化任务
- **智能推荐** — AI 根据任务内容推荐标签和优先级
- **任务分解** — 将复杂任务拆分为 3-7 个可执行的子任务
- **任务摘要** — 对所有当前任务生成汇总分析
- **Web 测试面板** — 浏览器直接打开，无需构建

### 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置 API 密钥
cp .env.example .env
# 修改 .env：设置 SILICONFLOW_API_KEY 和 DEFAULT_MODEL

# 启动后端
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
# API 地址: http://localhost:8000
# 交互文档: http://localhost:8000/docs

# 打开测试面板
# 双击 frontend/index.html 直接用浏览器打开
# 或使用 Python 内置服务器（另开一个终端）:
cd frontend && python -m http.server 8080
# 然后访问 http://localhost:8080
```

### API 文档

**任务管理**

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/tasks` | 创建任务 |
| GET | `/tasks` | 列出任务（支持 `?status=`、`?priority=`、`?tag=` 筛选） |
| GET | `/tasks/{id}` | 获取单个任务 |
| PUT | `/tasks/{id}` | 更新任务 |
| DELETE | `/tasks/{id}` | 删除任务 |

**AI 功能**

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/ai/parse-task` | 自然语言解析为任务 |
| POST | `/ai/suggest-tags` | 推荐标签 |
| POST | `/ai/suggest-priority` | 推荐优先级 |
| POST | `/ai/breakdown-task` | 分解复杂任务 |
| POST | `/ai/summarize-tasks` | 汇总所有任务 |

### 运行测试

```bash
pytest tests/ -v
```

### 项目结构

```
src/
  main.py           FastAPI 入口
  config.py         配置加载
  database.py       SQLite 数据库
  models/task.py    任务数据模型
  schemas/task.py   Pydantic 请求/响应模型
  services/
    ai_service.py   SiliconFlow API 客户端
    task_service.py 任务业务逻辑
  routes/
    tasks.py        任务 CRUD 接口
    ai.py           AI 功能接口
frontend/
  index.html        Web 测试面板（单文件，无需构建）
tests/
  conftest.py       pytest fixtures
  test_api.py       API 接口测试
  test_tasks.py     任务服务测试
```

### 注意事项
- AI 功能需要有效的 SiliconFlow API 密钥，可前往 [siliconflow.cn](https://siliconflow.cn) 免费获取。
- 模型名称通过 `.env` 中的 `DEFAULT_MODEL` 配置。
- 前端是纯 HTML 单文件，无需 npm 或任何构建工具。
