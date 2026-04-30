---
type: note
status: literature
created: 2026-04-29
source: https://github.com/aiming-lab/AutoResearchClaw
paper: ../Papers/AutoResearchClaw README.md
tags:
  - AI
  - autoresearch
  - agent
  - project
---

# AutoResearchClaw

一句话：
AutoResearchClaw 是 Karpathy autoresearch 思路的工程化扩展，目标是把自主研究从单次实验循环扩展到从 idea 到 paper 的完整流程。

## 本地资料

- 本地 README：[[AutoResearchClaw README.md|本地 README]]
- GitHub：https://github.com/aiming-lab/AutoResearchClaw

## 核心问题

- 原始 autoresearch 更像一个极简实验循环。
- 完整科研流程还需要构思、文献综述、实验设计、结果分析、写作、引用验证和人类审阅。
- 如果没有 HITL，人类很难在高风险节点把关。

## 方法

- 把研究拆成多个阶段：idea、literature review、hypothesis、experiment、analysis、paper writing、verification。
- 加入多种人机协作模式，例如 full-auto、gate-only、checkpoint、step-by-step、co-pilot。
- 强调 AI 生成的论文是 draft，需要人类 review。

## 我的理解

- 这个项目的价值在于把 Autoresearch 从“优化代码指标”推向“研究工作流管理”。
- 它更像工程平台，不是一篇单独论文。
- 对个人知识库来说，它可以作为未来“让 Codex 帮我做研究项目”的参考框架。

## 相关

- [[AI自我迭代研究范式：Autoresearch技术全景与产业洞察]]
