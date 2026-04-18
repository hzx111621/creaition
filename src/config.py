import os
from dotenv import load_dotenv

load_dotenv()

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY", "")
SILICONFLOW_BASE_URL = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")

# Available models: Pro, MiniMaxAI, MiniMax-M2.5
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "MiniMaxAI/MiniMax-M2.5")
DATABASE_URL = "sqlite:///./tasks.db"
