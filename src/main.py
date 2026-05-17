"""AuthFlow - Multi-agent authentication security audit pipeline."""
import asyncio
import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import Config
from .agents.scanner import AuthPatternScannerAgent
from .agents.auditor import SecurityAuditorAgent
from .agents.hardener import SecurityHardenerAgent
from .agents.reporter import SecurityReportGeneratorAgent

console = Console()


class AuthFlowPipeline:
    def __init__(self, config: Config):
        self.config = config
        self.scanner = AuthPatternScannerAgent(config)
        self.auditor = SecurityAuditorAgent(config)
        self.hardener = SecurityHardenerAgent(config)
        self.reporter = SecurityReportGeneratorAgent(config)

    async def run(self, target_path: str, output: str = "authflow_report.json"):
        console.print(Panel("[bold cyan]AuthFlow Pipeline[/bold cyan]", title="Authentication Security Audit"))

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Reading project...", total=None)

            target = Path(target_path)
            if target.is_file():
                codebase_info = target.read_text(encoding="utf-8")
            else:
                files = []
                for f in target.rglob("*"):
                    if f.is_file() and f.suffix in (".py", ".js", ".ts", ".go", ".java", ".yaml", ".yml", ".json"):
                        try:
                            files.append(f"--- {f.relative_to(target)} ---\n{f.read_text(encoding='utf-8')[:2000]}")
                        except Exception:
                            pass
                codebase_info = "\n\n".join(files[:20])

            # Agent 1: Scan
            progress.update(task, description="[cyan]Agent 1/4: Scanning auth patterns...[/cyan]")
            scan_result = await self.scanner.scan(codebase_info)
            progress.update(task, description="[green]Agent 1/4: Auth patterns scanned[/green]")

            # Agent 2: Audit
            progress.update(task, description="[cyan]Agent 2/4: Auditing security...[/cyan]")
            audit_result = await self.auditor.audit(scan_result, codebase_info)
            progress.update(task, description="[green]Agent 2/4: Security audited[/green]")

            # Agent 3: Harden
            progress.update(task, description="[cyan]Agent 3/4: Generating hardening...[/cyan]")
            hardening = await self.hardener.harden(audit_result, codebase_info)
            progress.update(task, description="[green]Agent 3/4: Hardening generated[/green]")

            # Agent 4: Report
            progress.update(task, description="[cyan]Agent 4/4: Generating report...[/cyan]")
            report = await self.reporter.generate_report(scan_result, audit_result, hardening)
            progress.update(task, description="[green]Agent 4/4: Report generated[/green]")

        final = {
            "pipeline": "AuthFlow",
            "scan": scan_result,
            "audit": audit_result,
            "hardening": hardening,
            "report": report,
        }
        Path(output).write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")

        table = Table(title="AuthFlow Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        if "risk_score" in report:
            table.add_row("Risk Score", str(report["risk_score"]))
        if "overall_risk_rating" in report:
            table.add_row("Risk Rating", report["overall_risk_rating"])
        if "metrics" in report:
            for k, v in report["metrics"].items():
                table.add_row(k, str(v))
        console.print(table)
        console.print(f"\n[bold green]Report saved to {output}[/bold green]")


@click.group()
def cli():
    pass


@cli.command()
@click.argument("target_path")
@click.option("--output", "-o", default="authflow_report.json", help="Output file")
def audit(target_path, output):
    """Audit authentication security."""
    config = Config()
    if not config.api_key:
        console.print("[red]Error: DEEPSEEK_API_KEY not set.[/red]")
        sys.exit(1)
    pipeline = AuthFlowPipeline(config)
    asyncio.run(pipeline.run(target_path, output))


if __name__ == "__main__":
    cli()
