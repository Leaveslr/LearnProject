---
type: note
status: literature
created: 2026-04-29
source: https://arxiv.org/abs/2508.07407
paper: ../Papers/Self-Evolving AI Agents Survey.pdf
tags:
  - AI
  - agent
  - survey
  - self-evolving
  - paper
---

# Self-Evolving AI Agents Survey

一句话：
这篇综述把 Self-Evolving AI Agents 定义为能够根据环境反馈持续优化自身组件的 Agent 系统，并用“输入、Agent 系统、环境、优化器”四组件反馈闭环统一解释现有方法。

## 本地资料

- PDF：[[Self-Evolving AI Agents Survey.pdf|本地 PDF]]
- arXiv：https://arxiv.org/abs/2508.07407
- GitHub：https://github.com/EvoAgentX/Awesome-Self-Evolving-Agents
- EvoAgentX：https://github.com/evoagentx/evoagentx

## 这篇论文要解决的问题

多数 Agent 系统部署后是静态的：

- prompt 是人写好的；
- tool list 是人配置好的；
- memory 结构是固定的；
- 多 Agent 拓扑和通信方式也是手工设计的。

但真实环境一直在变：

- 用户意图会变；
- 任务要求会变；
- 工具和知识源会变；
- 业务规则、医学知识、金融市场、代码库都会更新。

所以这篇综述关心的问题是：

```text
Agent 能不能不只是“被配置好以后执行任务”，
而是在运行中根据反馈持续改进自己的模型、提示、记忆、工具、工作流和协作结构？
```

## 核心定义

Self-evolving AI agents 是一类能够通过与环境交互，持续、系统地优化自身内部组件的自主系统。目标是在任务、上下文和资源变化时继续适应，同时保持安全并提升性能。

这里的“自演化”不只指模型权重更新，也包括：

- prompt 优化；
- memory 更新；
- tool use 策略优化；
- tool 创建；
- workflow / topology 优化；
- 多 Agent 通信协议优化；
- domain-specific reasoning strategy 优化。

## 三条设计约束

论文提出了 Self-Evolving AI Agents 的三条原则：

| 原则 | 含义 | 我理解的作用 |
|---|---|---|
| Endure | 修改过程中保持安全和稳定 | 先别把系统改坏 |
| Excel | 在安全前提下保持或提升性能 | 新版本不能退化 |
| Evolve | 在前两者约束下自主优化内部组件 | 系统要能自己适应变化 |

这三条有优先级：

```text
Endure > Excel > Evolve
```

也就是说，自主进化不能压过安全和性能保持。

## 从 MOP 到 MASE 的范式演进

论文把 LLM 系统的发展分成四个阶段：

| 阶段 | 名称 | 核心特点 |
|---|---|---|
| MOP | Model Offline Pretraining | 模型在静态数据上预训练，部署后基本冻结 |
| MOA | Model Online Adaptation | 部署后用 SFT、LoRA、RLHF 等方式适配 |
| MAO | Multi-Agent Orchestration | 多个 Agent 协作，但结构多由人设计 |
| MASE | Multi-Agent Self-Evolving | 多 Agent 系统根据环境反馈持续优化自身 |

这篇综述真正关心的是 MASE：Agent 不只是被调度，而是能持续改造自己的组件和协作方式。

## 整体框架：四组件反馈闭环

论文的核心框架是一个闭环：

```text
System Inputs
    ↓
Agent System
    ↓
Environment
    ↓
Optimiser
    ↓
更新 System Inputs 或 Agent System
    ↓
进入下一轮
```

它的意义是：所有自演化方法，本质上都可以看成“定义输入、运行 Agent、获得环境反馈、用优化器更新系统”的循环。

## 模块 1：System Inputs

功能：
定义 Agent 要解决什么问题，以及优化过程能看到哪些数据和约束。

常见形式：

- 任务描述；
- 训练集、验证集、测试集；
- 单个具体样例；
- 约束条件；
- 可用工具和资源；
- 上下文信息。

论文区分两类输入：

1. Task-level optimisation
   优化整个任务上的总体表现。例如让客服 Agent 在一批客服工单上平均成功率更高。

2. Instance-level optimisation
   针对单个样例优化。例如这个具体法律问题、这个具体 bug、这个具体医学病例。

它解决的问题：
没有输入边界，优化器不知道该为什么目标优化，也不知道什么数据能用。

## 模块 2：Agent System

功能：
这是被优化的主体，也就是实际执行任务的 Agent 或多 Agent 系统。

可以被优化的部分包括：

- foundation model / LLM；
- prompt；
- memory；
- tool-use policy；
- tool descriptions；
- workflow；
- multi-agent topology；
- inter-agent communication；
- agent role allocation。

在单 Agent 场景中，优化通常集中在：

- LLM 行为；
- prompt；
- memory；
- tool use。

在多 Agent 场景中，优化范围会扩大到：

- 每个 Agent 的角色；
- Agent 之间如何连接；
- 谁和谁通信；
- 信息流怎么走；
- 协作流程怎么组织。

它解决的问题：
Agent System 明确“到底要改谁”。否则自演化会变成一句空话。

## 模块 3：Environment

功能：
环境是 Agent 运行任务、执行动作、获得结果的地方。它提供反馈信号。

环境可以是：

- benchmark；
- 代码执行环境；
- GUI / 浏览器环境；
- 医疗诊断模拟器；
- 金融市场环境；
- 法律问答场景；
- 真实业务系统。

环境输出的反馈可以是：

- accuracy；
- F1；
- success rate；
- unit test pass rate；
- reward；
- cost；
- latency；
- human rating；
- LLM-as-a-judge score；
- safety violation signal。

它解决的问题：
没有环境反馈，Agent 只能“自我感觉良好”，不能形成真正的自演化。

## 模块 4：Optimiser

功能：
优化器根据环境反馈，决定如何更新 Agent System 或 System Inputs。

优化器由两个核心部分组成：

1. Search Space
   可以被搜索和修改的空间。

   例如：
   - prompt 候选；
   - tool selection；
   - memory structure；
   - LLM 参数；
   - workflow code；
   - multi-agent graph；
   - communication protocol。

2. Optimisation Algorithm
   如何在搜索空间里找更好的配置。

   例如：
   - rule-based heuristics；
   - gradient descent；
   - Bayesian optimisation；
   - MCTS；
   - reinforcement learning；
   - evolutionary algorithm；
   - learning-based policy；
   - LLM-generated proposal。

它解决的问题：
优化器是自演化的发动机。没有优化器，系统只能评估，不能改进。

## 单 Agent 优化

单 Agent 优化关注一个 Agent 内部组件如何变好。

### 1. LLM Behaviour Optimisation

目标：
提升模型的推理、规划和执行能力。

方法：

- SFT：用高质量 reasoning trajectory 微调。
- RL：用奖励信号训练模型生成更好的推理路径。
- Test-time scaling：不改参数，推理时生成多个候选或引入 verifier。

例子：
代码 Agent 生成多个修复方案，用测试结果筛选最好的方案。

### 2. Prompt Optimisation

目标：
自动找到更有效的 prompt。

方法：

- edit-based：对已有 prompt 做局部编辑；
- generative：让 LLM 直接生成新 prompt；
- text-gradient：用自然语言反馈当“梯度”指导修改；
- evolutionary：维护 prompt 种群，通过 mutation、crossover、selection 进化。

例子：
客服 Agent 失败案例显示“回答太笼统”，优化器生成新 prompt，要求先询问订单号和产品型号，再回答。

### 3. Memory Optimisation

目标：
让 Agent 在长任务和多轮交互中记住重要信息，忘掉无用信息。

方法：

- short-term memory：摘要、压缩、动态上下文筛选；
- long-term memory：RAG、数据库、知识图谱、用户偏好存储；
- memory update policy：决定何时写入、保留、合并、删除记忆。

例子：
个人助理 Agent 记住用户偏好的会议时间和写作风格，但不保存一次性的无关闲聊。

### 4. Tool Optimisation

目标：
让 Agent 更会用工具，甚至能创建工具。

方法：

- training-based：用工具调用轨迹训练模型；
- inference-time：推理时搜索工具调用路径；
- prompt-based：优化工具说明文档；
- reasoning-based：用树搜索、回溯、规划提升工具使用；
- tool creation：生成新的工具代码或工具文档。

例子：
数据分析 Agent 一开始只会调用 `read_csv`，后来发现任务常要画图，于是优化器加入或生成绘图工具，并更新 tool description。

## 多 Agent 优化

多 Agent 优化关注“Agent 团队”如何变好。

主要优化对象：

- prompt；
- topology；
- workflow；
- communication graph；
- LLM backbone 的协作能力。

### 1. Prompt Optimisation

为不同角色自动优化指令。

例子：
研究团队里，Reviewer Agent 的 prompt 会被优化成更严格地检查引用和实验设计。

### 2. Topology Optimisation

搜索 Agent 之间的连接方式。

常见结构：

- hierarchical；
- centralised；
- decentralised；
- graph-based；
- dynamic topology。

例子：
软件开发任务中，可能发现“Planner → Coder → Tester → Reviewer”的链式结构比所有 Agent 两两讨论更省成本。

### 3. Communication Optimisation

优化 Agent 之间说什么、什么时候说、用什么格式说。

例子：
让 Agent 用 JSON 输出任务状态，而不是长篇自然语言，可以降低 token 成本并减少歧义。

### 4. Unified Optimisation

同时优化 prompt、topology、workflow、工具和模型选择。

例子：
一个科研 Agent 系统同时调整：

- Literature Agent 的 prompt；
- Experiment Agent 的工具；
- Reviewer Agent 的检查标准；
- Agent 之间的通信顺序。

## 领域特定优化

论文强调，不同领域需要不同的自演化方式。

### 医疗

要求：

- 多轮问诊；
- 外部医学知识；
- 多模态信息；
- 高安全和可解释性。

优化重点：

- 医生角色分工；
- 诊断流程；
- 知识检索；
- 多 Agent 会诊。

### 编程

要求：

- 代码生成；
- 调试；
- 测试验证；
- 代码重构。

优化重点：

- self-feedback；
- tester / reviewer / executor 分工；
- 单元测试反馈；
- debug workflow。

### 金融与法律

要求：

- 规则约束；
- 外部知识；
- 高风险决策；
- 可解释推理。

优化重点：

- 专家角色；
- 检索器；
- controller；
- 规则 grounding；
- debate / court simulation。

## Evaluation：评估为什么也是核心模块

论文强调，评估不是最后一步，而是自演化系统的反馈来源。

评估方式包括：

- benchmark-based evaluation；
- tool/API agent evaluation；
- GUI/multimodal evaluation；
- domain-specific benchmarks；
- LLM-as-a-judge；
- Agent-as-a-judge；
- safety / alignment / robustness evaluation。

对 Self-Evolving Agent 来说，评估必须是持续的：

```text
每次更新 prompt、memory、tool、topology 之后，
都要检查性能是否提升，安全是否保持，成本是否可接受。
```

## 一个完整例子：自演化客服 Agent

假设我们要做一个客服 Agent，目标是提高工单解决率，同时降低错误回答。

### 第 0 轮：初始系统

System Inputs：

- 任务：处理电商售后问题。
- 数据：历史客服工单。
- 约束：不能承诺退款，除非满足政策条件。

Agent System：

- 一个 LLM；
- 一个客服 prompt；
- 一个订单查询工具；
- 一个退货政策文档；
- 简单 memory，记录当前对话。

Environment：

- 工单模拟器；
- 指标：解决率、用户满意度、错误承诺次数、平均轮次。

Optimiser：

- 搜索 prompt、工具说明和 memory 写入规则。
- 用 LLM 生成候选配置。
- 用 benchmark + LLM judge + policy checker 评估。

### 第 1 轮：发现问题

运行 100 条工单后发现：

- 解决率 62%；
- 错误承诺退款 8 次；
- 很多失败来自“用户没提供订单号，但 Agent 直接回答政策”。

Environment 返回反馈：

```text
缺少订单号时不应直接判断退款资格。
```

### 第 2 轮：优化 prompt

Optimiser 修改 prompt：

```text
如果用户询问退款、换货、物流异常，
必须先确认订单号和购买日期。
缺少关键信息时，只能询问补充信息，不能承诺结果。
```

重新评估：

- 错误承诺退款降到 2 次；
- 但平均轮次变长。

### 第 3 轮：优化工具

Optimiser 发现订单查询工具说明太长，Agent 经常漏参数。

更新 tool description：

```json
{
  "tool": "lookup_order",
  "required": ["order_id"],
  "optional": ["phone_last4"],
  "returns": ["purchase_date", "shipping_status", "refund_eligible"]
}
```

重新评估：

- 工具调用成功率提高；
- 平均轮次下降。

### 第 4 轮：优化 memory

系统发现用户在前面对话已经给过订单号，但 Agent 后面又问了一次。

Optimiser 更新 memory rule：

```text
把 order_id、purchase_date、issue_type 写入短期 memory；
当前会话结束后删除。
```

重新评估：

- 重复询问减少；
- 用户满意度提高。

### 第 5 轮：加入安全约束

Policy checker 发现有些回答仍然过度承诺。

加入 Endure 约束：

```text
任何包含“保证退款”“一定赔偿”的回答必须被拦截或改写。
```

最终系统形成闭环：

```text
工单数据 → 客服 Agent → 工单模拟器 → 指标和错误案例 → 优化 prompt/tool/memory/safety rule → 新 Agent
```

这就是 Self-Evolving AI Agent 的基本形态。

## 和 Bilevel Autoresearch 的关系

[[Bilevel Autoresearch Meta-Autoresearching Itself]] 是这篇综述框架里的一个具体案例。

对应关系：

| Survey 框架 | Bilevel Autoresearch 中的对应物 |
|---|---|
| System Inputs | GPT 预训练任务、参数空间、300 秒训练预算 |
| Agent System | 内层 autoresearch runner 和 LLM proposal loop |
| Environment | 训练脚本和 `val_bpb` 评估 |
| Optimiser | Level 1.5 策略调节 + Level 2 机制生成 |

Bilevel 的特殊之处是：

- 它不只优化 prompt、memory 或 tool；
- 它直接优化搜索机制本身；
- 它把 optimiser 也变成可被 LLM 修改的对象。

## 我自己的理解

这篇综述最有价值的地方不是列了很多论文，而是给了一个统一问题：

```text
一个 Agent 系统中，哪些东西可以被改？
谁来判断改得好不好？
用什么反馈来改？
怎样保证越改越安全、越有效？
```

对维护知识库也有启发：

- `Papers/` 存原始论文；
- `Notes/` 存读后的理解；
- `MOCs/` 存方向地图；
- `Daily/` 记录阅读过程；
- 每次读文献，都要问它对应四组件里的哪个模块。

## 局限

- 作为综述，它覆盖很广，但每个具体方法不会深入到实现细节。
- “自演化三定律”更像设计原则，不是可直接执行的工程标准。
- 很多自演化方法仍依赖人工设定搜索空间、评估指标和安全边界。
- 对长期运行中的安全、漂移、责任归属和监管问题，论文更多是提出方向，还没有成熟答案。

## 相关

- [[Bilevel Autoresearch Meta-Autoresearching Itself]]
- [[HyperAgents Meta-Level Self-Modifiable Agents]]
- [[SWE-RL Self-Play Reinforcement Learning for Software Engineering]]
- [[Ranking Engineer Agent REA]]
- [[AlphaEvolve A Coding Agent for Algorithmic Discovery]]
- [[AI自我迭代研究范式：Autoresearch技术全景与产业洞察]]
