"""AuthFlow Agent 2: Security Auditor."""
from .base import BaseAgent


class SecurityAuditorAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config, "SecurityAuditor")

    async def audit(self, scan_report: dict, codebase_info: str) -> dict:
        system_prompt = """You are a security auditor specializing in authentication and authorization.

Output JSON format:
{
    "owasp_findings": [
        {
            "category": "A01-A10",
            "title": "OWASP category title",
            "severity": "critical/high/medium/low",
            "description": "detailed finding",
            "evidence": "evidence from code",
            "remediation": "how to fix"
        }
    ],
    "cwe_mapping": [
        {
            "cwe_id": "CWE-XXX",
            "title": "CWE title",
            "affected_components": ["components"]
        }
    ],
    "authorization_issues": [
        {
            "type": "IDOR/privilege_escalation/missing_authz/broken_access",
            "description": "issue description",
            "impact": "potential impact"
        }
    ],
    "compliance_status": {
        "owasp_top10": "pass/fail/partial",
        "cwe_top25": "pass/fail/partial",
        "nist_800_63": "pass/fail/partial"
    },
    "risk_score": 0-100
}"""

        user_prompt = f"""Perform security audit on authentication system:

Scan Report: {scan_report}
Codebase: {codebase_info}

Conduct thorough security audit."""

        return await self.call_llm(system_prompt, user_prompt)
