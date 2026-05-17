"""Base agent for AuthFlow."""
import json
import httpx
from ..config import Config


class BaseAgent:
    def __init__(self, config: Config, name: str):
        self.config = config
        self.name = name

    async def call_llm(self, system_prompt: str, user_prompt: str) -> dict:
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            resp = await client.post(
                f"{self.config.api_base}/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.config.api_key}"},
                json={
                    "model": self.config.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": self.config.temperature,
                    "max_tokens": self.config.max_tokens,
                },
            )
            if resp.status_code != 200:
                print(f"[ERROR] API returned {resp.status_code}: {resp.text}")
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"raw_response": content}
