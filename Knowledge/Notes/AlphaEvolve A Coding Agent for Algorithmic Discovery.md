---
type: note
status: literature
created: 2026-04-29
source: https://arxiv.org/abs/2506.13131
paper: ../Papers/AlphaEvolve A Coding Agent for Algorithmic Discovery.pdf
tags:
  - AI
  - coding
  - algorithm-discovery
  - paper
---

# AlphaEvolve A Coding Agent for Algorithmic Discovery

一句话：
AlphaEvolve 用 LLM 生成代码、用进化式评估和选择循环改进算法，是自主研究范式在算法发现上的代表案例。

## 本地资料

- PDF：[[AlphaEvolve A Coding Agent for Algorithmic Discovery.pdf|本地 PDF]]
- arXiv：https://arxiv.org/abs/2506.13131

## 核心问题

- 算法发现很依赖人类直觉和长期试错。
- 只靠一次性生成代码很难稳定找到高质量算法。
- 如果能自动生成、评估、选择和变异代码，就能把算法设计变成持续搜索问题。

## 方法

- LLM 负责产生候选算法代码。
- 自动评估器检查正确性和性能。
- 进化循环保留更好的候选，继续变异和组合。
- 多智能体可以分别承担生成、评估、选择和变异职责。

## 我的理解

- AlphaEvolve 和自主研究范式的共同点是都把“提出方案、验证、保留改进”做成闭环。
- 区别在于 Autoresearch 常从训练流程或实验配置入手，AlphaEvolve 更直接优化算法本身。
- 它说明自主研究不只适合调参，也可能扩展到新算法发现。

## 相关

- [[AI自我迭代研究范式：Autoresearch技术全景与产业洞察]]
