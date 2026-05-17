# AuthFlow - Xiaomi 百万亿 Token 计划申请材料

## 04 字段文本

我构建了一个名为 **AuthFlow** 的多 Agent 协作认证安全审计系统，基于 Claude Code 开发、DeepSeek API 驱动。该项目解决的核心痛点是：认证授权代码涉及安全敏感操作（密码存储、令牌管理、会话控制），但人工审查难以全面覆盖 OWASP Top 10 和 CWE/SANS Top 25 安全标准，且认证漏洞的修复建议缺乏上下文关联。AuthFlow 通过 4 个角色分工明确的 AI Agent 实现认证扫描→安全审计→加固生成→报告输出的完整自动化闭环。

核心逻辑流采用长链推理架构：第一层 AuthPatternScannerAgent 对目标项目的所有认证相关代码进行深度扫描，识别认证机制类型（JWT/Session/OAuth2/API Key 等）、凭据处理方式和会话管理策略，按风险等级输出结构化扫描报告；第二层 SecurityAuditorAgent 消费扫描报告进行二次推理，对照 OWASP Top 10、CWE Top 25 和 NIST 800-63 等安全标准逐项审计，检测明文存储、SQL 注入、暴力破解、权限提升等漏洞并映射到具体 CWE 编号；第三层 SecurityHardenerAgent 根据审计结果生成具体的安全修复代码，包括密码哈希、参数化查询、速率限制、安全会话管理等加固措施，标注优先级和实施复杂度；第四层 SecurityReportGeneratorAgent 综合前三层结果生成包含风险评分、合规状态、修复路线图的综合安全报告。四个 Agent 间通信全部采用结构化 JSON，形成可追溯、可审计的审计链路。

项目使用 Python 构建，CLI 基于 Click + Rich 实现终端可视化。单次完整流水线运行消耗约 200-400 万 Token。该工具将认证安全审计从被动响应升级为主动防御，显著提升了系统的认证安全性和合规水平。

项目地址：https://github.com/dongjieliang8-blip/authflow
