"""AuthFlow Agent 3: Security Hardening Generator."""
from .base import BaseAgent


class SecurityHardenerAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config, "SecurityHardener")

    async def harden(self, audit_report: dict, codebase_info: str) -> dict:
        system_prompt = """You are a security hardening expert. Generate security fixes and hardening measures.

Output JSON format:
{
    "fixes": [
        {
            "finding_id": "reference to audit finding",
            "file": "file to modify",
            "current_code": "problematic code",
            "fixed_code": "hardened code",
            "explanation": "what was changed and why",
            "priority": "P0-P3"
        }
    ],
    "new_security_controls": [
        {
            "control": "control name",
            "implementation": "code implementation",
            "purpose": "what it protects against"
        }
    ],
    "configuration_hardening": [
        {
            "setting": "setting name",
            "current_value": "current",
            "recommended_value": "recommended",
            "reason": "why change"
        }
    ],
    "estimated_effort": {
        "critical_fixes": "X hours",
        "high_fixes": "X hours",
        "total": "X hours"
    }
}"""

        user_prompt = f"""Generate security hardening based on:

Audit Report: {audit_report}
Codebase: {codebase_info}

Generate concrete security fixes and hardening measures."""

        return await self.call_llm(system_prompt, user_prompt)
