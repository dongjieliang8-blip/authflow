"""AuthFlow Agent 4: Security Report Generator."""
from .base import BaseAgent


class SecurityReportGeneratorAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config, "SecurityReportGenerator")

    async def generate_report(self, scan_report: dict, audit_report: dict, hardening_report: dict) -> dict:
        system_prompt = """You are a security report writer. Generate comprehensive authentication security reports.

Output JSON format:
{
    "executive_summary": "high-level security posture summary",
    "overall_risk_rating": "critical/high/medium/low",
    "risk_score": 0-100,
    "key_findings": [
        {
            "finding": "description",
            "severity": "critical/high/medium/low",
            "business_impact": "impact description"
        }
    ],
    "compliance_summary": {
        "owasp_top10": {"status": "pass/fail", "details": "details"},
        "cwe_top25": {"status": "pass/fail", "details": "details"}
    },
    "remediation_roadmap": [
        {
            "phase": "Immediate/Short-term/Long-term",
            "items": ["action items"],
            "timeline": "timeline"
        }
    ],
    "metrics": {
        "total_vulnerabilities": N,
        "critical": N,
        "high": N,
        "medium": N,
        "low": N,
        "estimated_remediation_effort": "X hours"
    }
}"""

        user_prompt = f"""Generate comprehensive security report:

Scan Report: {scan_report}
Audit Report: {audit_report}
Hardening Report: {hardening_report}

Create an executive security report."""

        return await self.call_llm(system_prompt, user_prompt)
