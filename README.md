# AuthFlow

多 Agent 协作认证安全审计流水线，基于 Claude Code 开发、DeepSeek API 驱动。

## 核心架构

| Agent | 职责 | 输入 | 输出 |
|-------|------|------|------|
| AuthPatternScanner | 认证模式扫描 | 代码库 | 认证机制分析 |
| SecurityAuditor | 安全审计 | 扫描报告 | OWASP/CWE 审计报告 |
| SecurityHardener | 安全加固生成 | 审计报告 | 修复代码 + 配置 |
| SecurityReportGenerator | 安全报告生成 | 全部结果 | 综合安全报告 |

## 快速开始

```bash
pip install -r requirements.txt
copy .env.example .env
python -m src.main audit ./demo/ -o authflow_report.json
```

## 技术栈

- Python 3.10+ / Click / Rich / httpx / DeepSeek API

## 单次运行消耗

约 200-400 万 Token
