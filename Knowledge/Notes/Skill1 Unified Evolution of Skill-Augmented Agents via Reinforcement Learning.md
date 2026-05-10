---
type: note
status: literature
created: 2026-05-10
source: https://arxiv.org/abs/2605.06130
paper: ../Papers/Skill1 Unified Evolution of Skill-Augmented Agents via Reinforcement Learning.pdf
tags:
  - AI
  - agent
  - reinforcement-learning
  - skill-library
  - paper
---

# Skill1 Unified Evolution of Skill-Augmented Agents via Reinforcement Learning

一句话：
Skill1 把技能选择、技能使用和新技能蒸馏放进同一个强化学习闭环，让 Agent 的技能库围绕任务结果统一进化。

## 本地资料

- PDF：[[Skill1 Unified Evolution of Skill-Augmented Agents via Reinforcement Learning.pdf|本地 PDF]]
- arXiv：https://arxiv.org/abs/2605.06130
- Hugging Face：https://huggingface.co/papers/2605.06130

## 核心问题

- 长程 Agent 如果每次任务都从零开始，会浪费大量已有经验。
- 技能库可以沉淀可复用策略，但维护技能库并不只是“存技能”。
- 一个有效技能库至少需要三件事：选出相关技能、在执行中用好技能、从新轨迹里蒸馏新技能。
- 现有方法常把这三件事拆开优化，导致选择、使用和沉淀之间目标不一致。

## 方法

Skill1 的关键是训练一个单一策略，让三种能力共同围绕任务结果优化：

- 先生成查询，用来检索已有技能库。
- 对候选技能重排，选出当前任务最相关的技能。
- 在技能条件下执行任务。
- 从执行轨迹中蒸馏新的技能，回写到技能库。

学习信号只来自任务结果。论文把任务结果的低频趋势用于给技能选择分配信用，把高频变化用于给技能蒸馏分配信用，从而避免为不同阶段设计独立奖励。

## 实验结果

- 在 ALFWorld 和 WebShop 上，Skill1 超过既有技能型 Agent 和强化学习 baseline。
- 训练动态显示，技能选择、技能使用和技能蒸馏会一起改善。
- 消融实验表明，移除任一 credit signal 都会破坏整体进化效果。

## 我的理解

这篇论文的重点不是“给 Agent 一个技能库”，而是把技能库当作一个会随任务经验更新的外部记忆系统。

如果只优化技能选择，Agent 会越来越会查库，但技能质量不一定提升；如果只优化技能蒸馏，库里可能塞进很多不稳定或不匹配的策略。Skill1 的价值在于把“查什么、怎么用、留下些什么”绑定到同一个任务成败信号上。

对实际系统来说，这很像一个可持续运营的经验库：每次任务既消费经验，也生产经验，而且需要有机制判断哪些经验真的值得沉淀。

## 可借鉴点

- 技能库不应只是静态 prompt 集合，而应有任务驱动的更新机制。
- 对 Agent 训练可以把技能查询、技能使用、经验沉淀视为同一条轨迹上的不同决策。
- 如果做企业内部 Agent，可以把成功任务轨迹蒸馏成可检索 SOP，再用后续任务结果反向筛选 SOP 质量。

## 相关

- [[Self-Evolving AI Agents Survey]]
- [[AutoResearchClaw]]
