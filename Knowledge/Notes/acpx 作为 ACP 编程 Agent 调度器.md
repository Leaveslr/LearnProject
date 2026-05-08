---
type: note
status: evergreen
created: 2026-05-08
source: https://github.com/openclaw/acpx
tags:
  - AI
  - agent
  - ACP
  - Claude-Code
  - workflow
---

# acpx 作为 ACP 编程 Agent 调度器

一句话：
acpx 是一个面向程序调用的 ACP 客户端，它把 Claude Code、Codex、Gemini 等编程 Agent 包装成可脚本化、可排队、可持久会话的命令行接口。

## 核心定位

- acpx 不是模型，也不是 Claude Code 本身。
- 它的角色是 headless ACP client：负责启动 Agent adapter、维护 ACP JSON-RPC 连接、保存 session、处理权限、转发文件和终端能力、管理任务队列。
- 真正思考和改代码的是后面的 Claude Code、Codex、Gemini 等 Agent。
- 它适合脚本、自动化、队列任务、日志记录和多 Agent 统一调度，不适合替代人类交互式聊天 UI。

## 调用链路

以 Claude 为例：

```text
用户或脚本
  -> acpx
  -> claude-agent-acp adapter
  -> Claude Code
  -> 文件读写、命令执行、测试运行
  -> acpx 输出结果
```

对应命令：

```bash
npx acpx claude exec "帮我总结当前项目"
```

使用自动批准：

```bash
npx acpx --approve-all --format quiet claude exec "帮我写个计算加法的脚本，并写个测试脚本，执行"
```

## 和直接使用 Claude Code CLI 的区别

直接运行：

```bash
claude
```

更像人类交互入口，适合边看边聊、手动确认、观察 diff、连续对话。

通过 acpx：

```bash
npx acpx claude exec "执行一个明确任务"
```

更像程序调用入口，适合脚本、批处理、日志、队列和自动工作流。

两者背后都可以使用 Claude Code 的能力，但会话、权限处理和输出形式不完全一样。

## Agent adapter 是什么

acpx 不直接调用 Anthropic HTTP API。

它会根据 agent 名称找到对应 adapter，例如 Claude：

```text
claude = npx -y @agentclientprotocol/claude-agent-acp
```

adapter 的作用是把标准 ACP 消息转换成 Claude Code 能理解和执行的动作。acpx 和 adapter 之间通过 stdin/stdout 传 JSON-RPC 消息。

## 权限策略

常用策略：

- `--approve-all`：自动批准所有权限请求，包括写文件和执行命令。
- `--approve-reads`：自动批准读文件和搜索，写入和执行仍需要确认。
- `--deny-all`：拒绝所有权限请求。

日常自动化可以用：

```bash
npx acpx --approve-all --format quiet claude exec "任务描述"
```

但长期使用时更适合给 Claude Code 设置项目级白名单，例如只允许 `npm test`、`node`、`git diff` 等低风险命令。

## 顺序执行和队列

acpx 支持同一个 session 内排队执行任务。

示例：

```bash
acpx claude sessions ensure --name work
acpx claude -s work --no-wait "第一步：阅读项目结构"
acpx claude -s work --no-wait "第二步：检查潜在问题"
acpx claude -s work --no-wait "第三步：给出修改建议"
```

这些任务会进入同一个 session 的队列，按顺序执行。

注意：这不是让 Claude 自动无限循环直到完成。是否继续下一轮，需要通过 prompt、外层脚本或 `acpx flow run` 显式设计。

## 输出和日志

普通调用会直接输出到终端：

```bash
node scripts/call-claude-acp.mjs "请总结当前项目"
```

保存结果：

```bash
node scripts/call-claude-acp.mjs "请总结当前项目" > claude-result.txt
```

保存完整执行过程：

```bash
mkdir -p logs
npx acpx --approve-all --format quiet claude exec "帮我写个计算加法的脚本，并写个测试脚本，执行" > logs/claude-acp-addition-run.log 2>&1
```

## 本地已经创建的辅助脚本

ACP 调用脚本：

```bash
node scripts/call-claude-acp.mjs "你的问题"
```

直连 Anthropic API 脚本：

```bash
ANTHROPIC_API_KEY="sk-ant-..." node scripts/call-claude.mjs "你的问题"
```

两者区别：

- `scripts/call-claude-acp.mjs`：通过 `acpx -> Claude ACP adapter -> Claude Code`。
- `scripts/call-claude.mjs`：直接请求 Anthropic Messages API。

## 适合的日常用法

- 临时让 Claude Code 执行一个明确任务，并把日志保存下来。
- 把多步任务排进同一个 session，让它顺序执行。
- 用 `--approve-all` 快速跑低风险实验。
- 用 `--format json` 做更结构化的程序集成。
- 用 `flow` 把「调用 Agent -> 跑命令 -> 再调用 Agent」写成自动化流程。

## 风险提醒

- `--approve-all` 会自动允许写文件和执行命令，适合可信项目或隔离环境。
- 如果任务可能涉及删除文件、推送代码、读取密钥、安装未知包，应避免全自动批准。
- 建议配合日志保存，方便复盘 Agent 做了什么。

## 来源

- GitHub：<https://github.com/openclaw/acpx>
- CLI 文档：<https://github.com/openclaw/acpx/blob/main/docs/CLI.md>
- Claude Code permissions：<https://code.claude.com/docs/en/permission-modes>

## 相关

- [[AutoResearchClaw]]
