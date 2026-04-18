import os
import json
from openai import OpenAI, APIError

from src.config import SILICONFLOW_API_KEY, SILICONFLOW_BASE_URL, DEFAULT_MODEL

class AIService:
    def __init__(self):
        if not SILICONFLOW_API_KEY:
            raise RuntimeError("SILICONFLOW_API_KEY is not set. Please configure it in .env")
        self.client = OpenAI(
            api_key=SILICONFLOW_API_KEY,
            base_url=SILICONFLOW_BASE_URL,
        )
        self.model = DEFAULT_MODEL

    def chat(self, messages: list[dict], model: str | None = None) -> str:
        try:
            response = self.client.chat.completions.create(
                model=model or self.model,
                messages=messages,
                temperature=0.3,
            )
            return response.choices[0].message.content or ""
        except APIError as e:
            raise RuntimeError(f"SiliconFlow API error: {e}")

    def parse_task_from_natural_language(self, text: str) -> dict:
        prompt = f"""你是一个任务解析助手。根据用户输入的自然语言描述，提取任务信息。

用户输入: "{text}"

请以 JSON 格式返回，字段如下：
- title: 任务标题（必填，简洁）
- description: 任务描述（可选）
- priority: 优先级，可选值 "low", "medium", "high"
- tags: 标签数组（可选，1-3个标签，字符串）
- due_date: 截止日期（可选，ISO格式 YYYY-MM-DD，如果没提到则不返回此字段）

只返回 JSON，不要有其他内容。示例：
{{"title": "完成报告", "description": "需要整理 Q1 数据", "priority": "high", "tags": ["工作", "报告"]}}"""
        content = self.chat([{"role": "user", "content": prompt}])
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"title": text, "description": "", "priority": "medium", "tags": []}

    def suggest_tags(self, title: str, description: str = "") -> list[str]:
        prompt = f"""根据以下任务内容，推荐 1-3 个合适的标签。

任务标题: {title}
任务描述: {description or "无"}

请以 JSON 数组格式返回标签列表，只返回数组，不要有其他内容。示例：
["工作", "紧急", "会议"]"""
        content = self.chat([{"role": "user", "content": prompt}])
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return []

    def suggest_priority(self, title: str, description: str = "") -> str:
        prompt = f"""分析以下任务的紧急程度，推荐优先级。

任务标题: {title}
任务描述: {description or "无"}

只返回一个词: low、medium 或 high。不要有其他内容。"""
        content = self.chat([{"role": "user", "content": prompt}])
        content = content.strip().lower()
        if content in ("low", "medium", "high"):
            return content
        return "medium"

    def breakdown_task(self, title: str, description: str = "") -> list[dict]:
        prompt = f"""将以下复杂任务拆分为 3-7 个简单的子任务。

任务标题: {title}
任务描述: {description or "无"}

请以 JSON 数组格式返回子任务列表，每个子任务包含 title 和 priority 字段。示例：
[{{"title": "收集数据", "priority": "high"}}, {{"title": "整理报告", "priority": "medium"}}]

只返回 JSON，不要有其他内容。"""
        content = self.chat([{"role": "user", "content": prompt}])
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return []

    def summarize_tasks(self, tasks: list[dict]) -> str:
        if not tasks:
            return "当前没有待处理的任务。"
        task_list = "\n".join(
            f"- [{t['status']}] {t['title']} (优先级: {t['priority']}, 标签: {', '.join(t['tags'])})"
            for t in tasks
        )
        prompt = f"""以下是目前的所有任务，请生成一个简洁的摘要：

{task_list}

请用 2-3 句话总结当前任务状态，突出重点和紧急事项。用中文回复。"""
        return self.chat([{"role": "user", "content": prompt}])

_ai_service: AIService | None = None

def get_ai_service() -> AIService:
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
