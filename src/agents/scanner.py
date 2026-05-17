"""AuthFlow Agent 1: Authentication Pattern Scanner."""
from .base import BaseAgent


class AuthPatternScannerAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config, "AuthPatternScanner")

    async def scan(self, codebase_info: str) -> dict:
        system_prompt = """You are an authentication security expert. Scan codebase for authentication patterns and vulnerabilities.

Output JSON format:
{
    "auth_mechanisms": [
        {
            "type": "jwt/session/oauth2/api_key/basic/saml/oidc",
            "location": "file/function",
            "implementation": "description",
            "risk_level": "critical/high/medium/low"
        }
    ],
    "credential_handling": {
        "storage": ["how credentials are stored"],
        "transmission": ["how credentials are transmitted"],
        "rotation": "credential rotation policy",
        "issues": ["security issues found"]
    },
    "session_management": {
        "type": "stateful/stateless",
        "timeout": "session timeout config",
        "issues": ["session security issues"]
    },
    "vulnerabilities": [
        {
            "type": "vulnerability type",
            "severity": "critical/high/medium/low",
            "location": "file:line",
            "description": "vulnerability description"
        }
    ]
}"""

        user_prompt = f"""Scan this codebase for authentication patterns and vulnerabilities:

{codebase_info}

Identify all auth mechanisms and security issues."""

        return await self.call_llm(system_prompt, user_prompt)
