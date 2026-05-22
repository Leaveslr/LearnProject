---
type: note
status: literature
created: 2026-05-12
source: https://arxiv.org/abs/2605.03042
paper: ../Papers/ARIS Autonomous Research via Adversarial Multi-Agent Collaboration.pdf
tags:
  - AI
  - autoresearch
  - multi-agent
  - research-harness
  - paper
---

# ARIS Autonomous Research via Adversarial Multi-Agent Collaboration

一句话：
ARIS 把自主科研看成一个 research harness 问题：长期研究代理的效果不只取决于模型权重，还取决于工作流编排、记忆检索、跨模型审稿和证据到 claim 的保障机制。

## 本地资料

- PDF：[[ARIS Autonomous Research via Adversarial Multi-Agent Collaboration.pdf|本地 PDF]]
- arXiv：https://arxiv.org/abs/2605.03042
- Hugging Face Papers：https://huggingface.co/papers/2605.03042
- 项目：https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep

## 核心问题

- 长周期研究代理最危险的失败形态不一定是明显崩溃，而是“看起来成功但证据不充分”：实验可能是真的，但被错误转述；论文 claim 可能超过证据许可范围；后续读者会继承 executor 的叙事框架。
- 同一模型自我反思容易保留相关偏差。ARIS 的默认假设更保守：单代理长期任务默认不可靠，需要把工作拆成可审计子流程，并引入不同模型家族的独立 reviewer。
- 对自主科研来说，关键资产不只是 prompt 或模型，而是围绕模型的 harness：哪些信息被保存、检索、展示，哪些产物必须过关，哪些 claim 可以进入论文。

## 方法

- **执行层**：65+ 个 Markdown 定义的 research skills，MCP 模型与工具桥接，项目级 research wiki，确定性图表生成。
- **编排层**：五个端到端 workflow：idea discovery、experiment bridge、auto review loop、paper writing、rebuttal；支持不同 effort level 和 reviewer 路由。
- **保障层**：三阶段证据检查：实验完整性验证、result-to-claim 映射、paper claim audit；另有五轮科学编辑、数学证明检查和 PDF 视觉检查。
- **跨模型对抗协作**：executor 推进研究，reviewer 从不同模型家族审查中间产物并要求修改，避免同源自检盲点。
- **原型自改进循环**：记录研究 trace，提出 skill prompt、默认配置和收敛规则改进，但只有 reviewer 批准后才采用。

## 早期部署经验

- 技能库从早期 21 个 core skills 扩展到 65+，覆盖机器人、硬件设计、通信、数学证明、基金申请、演示生成等方向。
- 论文记录了一次约 8 小时 overnight run：完成 4 轮 review-revise，将内部 reviewer 分数从 5.0 提升到 7.5/10，启动 20+ 个 GPU 实验，并删除缺乏证据支持的 claim。
- 作者明确说明这些结果是观察性部署经验，不能因果归因于 ARIS；跨模型 review 是否优于同模型 review 仍需要 compute-matched benchmark。

## 我的理解

- ARIS 的贡献不是“再做一个自动写论文代理”，而是把 Autoresearch 的关注点从实验闭环扩展到**证据治理和研究状态管理**。
- 它补上了 AutoResearchClaw 和 REA 之间的一块拼图：AutoResearchClaw 强调 idea-to-paper 流水线，REA 强调生产级异步实验，ARIS 强调研究 claim 如何被独立审计、复用和追责。
- 对 Autoresearch 技术栈来说，ARIS 提醒我们：长期自主研究的瓶颈可能不是模型会不会写代码，而是系统能否维护可靠记忆、清晰 provenance 和可反驳的 claim ledger。

## 相关

- [[AI自我迭代研究范式：Autoresearch技术全景与产业洞察]]
- [[AutoResearchClaw]]
- [[Ranking Engineer Agent REA]]
- [[Bilevel Autoresearch Meta-Autoresearching Itself]]
