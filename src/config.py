"""AuthFlow configuration."""
import os
from pathlib import Path
from dataclasses import dataclass


def _load_dotenv():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


@dataclass
class Config:
    api_key: str = ""
    api_base: str = "https://token-plan-cn.xiaomimimo.com"
    model: str = "mimo-v2.5"
    temperature: float = 0.3
    max_tokens: int = 4096
    timeout: int = 120

    def __post_init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY", self.api_key)
        self.api_base = os.getenv("DEEPSEEK_API_BASE", self.api_base)
        self.model = os.getenv("DEEPSEEK_MODEL", self.model)
