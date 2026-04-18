import pytest
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ.setdefault("SILICONFLOW_API_KEY", "test-key")
os.environ.setdefault("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
os.environ.setdefault("DEFAULT_MODEL", "MiniMaxAI/MiniMax-M2.5")

pytest_plugins = ["pytest_asyncio"]

from src.main import app
from src.database import init_db, get_db_connection

@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    init_db()
    with get_db_connection() as conn:
        conn.execute("DELETE FROM tasks")
        conn.commit()
    yield
    with get_db_connection() as conn:
        conn.execute("DELETE FROM tasks")
        conn.commit()
