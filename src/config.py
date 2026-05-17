"""AuthFlow configuration."""
import os
from dataclasses import dataclass


@dataclass
class Config:
    api_key: str = ""
    api_base: str = "https://api.deepseek.com"
    model: str = "deepseek-chat"
    temperature: float = 0.3
    max_tokens: int = 4096
    timeout: int = 120

    def __post_init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY", self.api_key)
        self.api_base = os.getenv("DEEPSEEK_API_BASE", self.api_base)
        self.model = os.getenv("DEEPSEEK_MODEL", self.model)
