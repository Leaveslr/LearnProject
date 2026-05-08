# ICLR 2026: LLM / Agent / 自我改进主题笔记

来源: https://iclr.cc/virtual/2026/papers.html

整理时间: 2026-05-06

范围说明: 只看 ICLR 2026 主会里和 LLM、Agent、post-training、reasoning、自我改进、test-time adaptation、agent memory、tool use、alignment/safety 相关的论文。其它方向如纯视觉、纯生成模型、科学计算、机器人等暂不展开。

## 总体判断

ICLR 2026 里和 LLM / Agent / 自我改进相关的论文，可以看成 7 条主线:

1. Post-training / alignment: 如何用 preference、reward、DPO、rubric、data selection 改进 LLM。
2. Agent memory / long-context: 如何让 agent 记住长期信息，并在多轮任务里稳定使用上下文。
3. Tool use / multi-agent / workflow: 如何让 agent 学会调用工具、协作、规划和适应环境。
4. Self-improvement / test-time adaptation: 如何让模型或 agent 在测试时、交互中、探索中继续变强。
5. Reasoning model post-training: 如何训练、压缩、验证和对齐 reasoning / CoT 能力。
6. Prompt / instruction / data selection: 如何构造更好的指令、prompt、训练数据和 agent 数据协议。
7. Safety risks: 自我改进和 agent 化之后的 prompt injection、jailbreak、mis-evolution、安全监控和 unlearning。

这条线和 RSI Workshop 的联系很强: 主会更像是把“自我改进”的组件拆开研究，workshop 更直接讨论 recursive/self-evolving loop。

## 子主题 1: Post-training / Alignment / Preference / Reward

核心问题: LLM 在预训练之后，如何用更少、更好、更可解释的反馈继续提升？这里的关键词是 preference data、reward model、DPO、rubric、RLHF、fine-tuning。

代表论文:

1. [ActiveDPO: Active Direct Preference Optimization for Sample-Efficient Alignment](https://iclr.cc/virtual/2026/poster/10009521)
2. [Chasing the Tail: Effective Rubric-based Reward Modeling for Large Language Model Post-Training](https://iclr.cc/virtual/2026/poster/10007351)
3. [Data Selection for LLM Alignment Using Fine-Grained Preferences](https://iclr.cc/virtual/2026/poster/10007475)
4. [When Weak LLMs Speak with Confidence, Preference Alignment Gets Stronger](https://iclr.cc/virtual/2026/poster/10009497)
5. [Towards Understanding Valuable Preference Data for Large Language Model Alignment](https://iclr.cc/virtual/2026/poster/10010595)
6. [Verification and Co-Alignment via Heterogeneous Consistency for Preference-Aligned LLM Annotations](https://iclr.cc/virtual/2026/poster/10007842)
7. [PALC: Preference Alignment via Logit Calibration](https://iclr.cc/virtual/2026/poster/10011917)
8. [Robust Preference Alignment via Directional Neighborhood Consensus](https://iclr.cc/virtual/2026/poster/10007833)
9. [Uni-DPO: A Unified Paradigm for Dynamic Preference Optimization of LLMs](https://iclr.cc/virtual/2026/poster/10010533)
10. [RiskPO: Risk-based Policy Optimization with Verifiable Reward for LLM Post-Training](https://iclr.cc/virtual/2026/poster/10010102)
11. [Stackelberg Learning from Human Feedback: Preference Optimization as a Sequential Game](https://iclr.cc/virtual/2026/poster/10006802)
12. [What's In My Human Feedback? Learning Interpretable Descriptions of Preference Data](https://iclr.cc/virtual/2026/poster/10007081)

阅读重点:

- Preference data 不是越多越好，关键是哪些反馈“有价值”。
- Rubric-based reward modeling 可能成为更可解释、更可扩展的 post-training 路线。
- DPO/RLHF 正在从单一偏好优化走向 active、dynamic、risk-aware、game-theoretic。
- Weak model 或自动标注反馈能否可靠增强 stronger model，是值得重点追的方向。

## 子主题 2: Agent Memory / Long-context / Multi-turn

核心问题: Agent 的长期能力不只来自更长上下文，还来自可检索、可回看、可压缩、可训练的记忆机制。

代表论文:

1. [MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent](https://iclr.cc/virtual/2026/poster/10007825)
2. [Look Back to Reason Forward: Revisitable Memory for Long-Context LLM Agents](https://iclr.cc/virtual/2026/poster/10011811)
3. [Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions](https://iclr.cc/virtual/2026/poster/10010781)
4. [GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs](https://iclr.cc/virtual/2026/poster/10008792)
5. [Q-RAG: Long Context Multi-Step Retrieval via Value-Based Embedder Training](https://iclr.cc/virtual/2026/poster/10009944)
6. [Beyond RAG vs. Long-Context: Learning Distraction-Aware Retrieval for Efficient Knowledge Grounding](https://iclr.cc/virtual/2026/poster/10008538)
7. [BrowseNet: Graph-Based Associative Memory for Contextual Information Retrieval](https://iclr.cc/virtual/2026/poster/10011699)
8. [UltraMemV2: Memory Networks Scaling to 120B Parameters with Superior Long-Context Learning](https://iclr.cc/virtual/2026/poster/10009579)
9. [RMAAT: Astrocyte-Inspired Memory Compression and Replay for Efficient Long-Context Transformers](https://iclr.cc/virtual/2026/poster/10007054)
10. [LLMs Get Lost In Multi-Turn Conversation](https://iclr.cc/virtual/2026/poster/10009146)
11. [Let's (not) just put things in Context: Test-time Training for Long-context LLMs](https://iclr.cc/virtual/2026/poster/10010442)
12. [SPELL: Self-Play Reinforcement Learning for Evolving Long-Context Language Models](https://iclr.cc/virtual/2026/poster/10011237)
13. [InftyThink: Breaking the Length Limits of Long-Context Reasoning in Large Language Models](https://iclr.cc/virtual/2026/poster/10009358)
14. [SoLoPO: Unlocking Long-Context Capabilities in LLMs via Short-to-Long Preference Optimization](https://iclr.cc/virtual/2026/poster/10007940)

阅读重点:

- “长上下文”不等于“会记忆”，多轮对话里模型仍可能迷失。
- Agent memory 正在从简单 RAG 走向可训练 memory policy、graph memory、revisitable memory。
- Long-context 能力可以通过 self-play、test-time training、short-to-long preference optimization 来增强。
- 记忆系统的评测会越来越重要，因为 agent 的真实任务往往是持续多轮、跨上下文的。

## 子主题 3: Tool Use / Multi-agent / Workflow

核心问题: Agent 不只是回答问题，而是在环境中计划、调用工具、修正流程、协作和完成长期任务。

代表论文:

1. [GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs](https://iclr.cc/virtual/2026/poster/10008792)
2. [ResiliBench: Evaluating Agentic Workflow Adaptation in Stochastic Environments](https://iclr.cc/virtual/2026/poster/10010130)
3. [ATLAS: Constraints-Aware Multi-Agent Collaboration for Real-World Travel Planning](https://iclr.cc/virtual/2026/poster/10007591)
4. [TUMIX: Multi-Agent Test-Time Scaling with Tool-Use Mixture](https://iclr.cc/virtual/2026/poster/10010417)
5. [In-the-Flow Agentic System Optimization for Effective Planning and Tool Use](https://iclr.cc/virtual/2026/poster/10009931)
6. [OrchestrationBench: LLM-Driven Agentic Planning and Tool Use in Multi-Domain Scenarios](https://iclr.cc/virtual/2026/poster/10009754)
7. [FlowSearcher: Synthesizing Memory-Guided Agentic Workflows for Web Information Seeking](https://iclr.cc/virtual/2026/poster/10011673)
8. [WALT: Web Agents that Learn Tools](https://iclr.cc/virtual/2026/poster/10008481)
9. [Dynamic Speculative Agent Planning](https://iclr.cc/virtual/2026/poster/10008884)
10. [Multi-Agent Guided Policy Optimization](https://iclr.cc/virtual/2026/poster/10009778)
11. [Multi-Agent Debate with Memory Masking](https://iclr.cc/virtual/2026/poster/10010659)
12. [Real-Time Reasoning Agents in Evolving Environments](https://iclr.cc/virtual/2026/poster/10007516)
13. [Don't Just Fine-tune the Agent, Tune the Environment](https://iclr.cc/virtual/2026/poster/10007443)
14. [CoAct-1: Computer-using Multi-agent System with Coding Actions](https://iclr.cc/virtual/2026/poster/10007725)
15. [CoMAS: Co-Evolving Multi-Agent Systems via Interaction Rewards](https://iclr.cc/virtual/2026/poster/10007941)

阅读重点:

- Agent 研究正在从“单模型能力”转向“workflow 和环境共同优化”。
- Tool-use mixture、workflow synthesis、agentic routing 是提高 agent 能力的重要方法。
- Multi-agent 方向不只是 debate，也包括协作、任务分工、通信、routing、collective reward。
- “调环境”可能和“调模型”一样重要，这是 agent 工程里很实用的一条线。

## 子主题 4: Self-improvement / Test-time Adaptation / Curriculum

核心问题: 模型能否在测试时、任务交互中、探索中继续学习？这条线最接近 recursive self-improvement。

代表论文:

1. [Test-Time Adaptation for LLM Agents via Environment Interaction](https://iclr.cc/virtual/2026/poster/10009800)
2. [EvoTest: Evolutionary Test-Time Learning for Self-Improving Agentic Systems](https://iclr.cc/virtual/2026/poster/10010217)
3. [Towards Self-Evolving Agent Benchmarks : Validatable Agent Trajectory via Test-Time Exploration](https://iclr.cc/virtual/2026/poster/10011762)
4. [R-Zero: Self-Evolving Reasoning LLM from Zero Data](https://iclr.cc/virtual/2026/poster/10011147)
5. [Prompt Curriculum Learning for Efficient LLM Post-Training](https://iclr.cc/virtual/2026/poster/10006420)
6. [TUMIX: Multi-Agent Test-Time Scaling with Tool-Use Mixture](https://iclr.cc/virtual/2026/poster/10010417)
7. [Scaling Synthetic Task Generation for Agents via Exploration](https://iclr.cc/virtual/2026/poster/10007463)
8. [CaTS: Calibrated Test-Time Scaling for Efficient LLM Reasoning](https://iclr.cc/virtual/2026/poster/10007848)
9. [ReVeal: Self-Evolving Code Agents via Reliable Self-Verification](https://iclr.cc/virtual/2026/poster/10007284)
10. [ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory](https://iclr.cc/virtual/2026/poster/10007887)
11. [MemGen: Weaving Generative Latent Memory for Self-Evolving Agents](https://iclr.cc/virtual/2026/poster/10006821)
12. [Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents](https://iclr.cc/virtual/2026/poster/10007327)
13. [Best-of-Infinity: Asymptotic Performance of Test-Time LLM Ensembling](https://iclr.cc/virtual/2026/poster/10011606)
14. [Your Agent May Misevolve: Emergent Risks in Self-evolving LLM Agents](https://iclr.cc/virtual/2026/poster/10010580)

阅读重点:

- Test-time scaling 不再只是多采样/投票，而是工具混合、环境交互、轨迹探索、任务生成。
- Self-evolving agent 需要可靠验证，否则会出现 misevolve，也就是越学越偏。
- Code agent 是自我改进的天然实验场，因为可以通过测试、验证器和执行结果形成闭环。
- Zero-data/self-generated data 是非常值得跟进的路线，和 RSI workshop 里的 self-play 论文呼应。

## 子主题 5: Reasoning Model Post-training

核心问题: Reasoning model 的 CoT、verifier、RLVR、长推理链该如何训练和验证？这些能力如何与安全对齐兼容？

代表论文:

1. [Verifying Chain-of-Thought Reasoning via Its Computational Graph](https://iclr.cc/virtual/2026/poster/10010813)
2. [FaithCoT-Bench: Benchmarking Instance-Level Faithfulness of Chain-of-Thought Reasoning](https://iclr.cc/virtual/2026/poster/10007686)
3. [Are Reasoning LLMs Robust to Interventions on their Chain-of-Thought?](https://iclr.cc/virtual/2026/poster/10008704)
4. [Reasoning Models Can be Accurately Pruned Via Chain-of-Thought Reconstruction](https://iclr.cc/virtual/2026/poster/10006931)
5. [Pruning Long Chain-of-Thought of Large Reasoning Models via Small-Scale Preference Optimization](https://iclr.cc/virtual/2026/poster/10011162)
6. [AdvChain: Adversarial Chain-of-Thought Tuning for Robust Safety Alignment of Large Reasoning Models](https://iclr.cc/virtual/2026/poster/10007590)
7. [Reinforcing General Reasoning Without Verifiers](https://iclr.cc/virtual/2026/poster/10007455)
8. [DAG-Math: Graph-of-Thought Guided Mathematical Reasoning in LLMs](https://iclr.cc/virtual/2026/poster/10006522)
9. [Quantile Advantage Estimation: Stabilizing RLVR for LLM Reasoning](https://iclr.cc/virtual/2026/poster/10009065)
10. [CoT Vectors: Transferring and Probing the Reasoning Mechanisms of LLMs](https://iclr.cc/virtual/2026/poster/10010072)
11. [Beyond Magnitude: Leveraging Direction of RLVR Updates for LLM Reasoning](https://iclr.cc/virtual/2026/poster/10007176)
12. [Long Chain-of-Thought Reasoning Across Languages](https://iclr.cc/virtual/2026/poster/10011704)

阅读重点:

- CoT 的“可读性”和“真实性”不是一回事，faithfulness 和 intervention robustness 会越来越关键。
- RLVR 正在成为 reasoning post-training 的核心训练范式之一。
- 长 CoT 需要压缩、剪枝、重构，否则推理成本会变高，也可能引入噪声。
- Safety alignment 不能只在最终答案上做，推理链本身也可能被攻击或失真。

## 子主题 6: Prompt / Instruction / Data Selection

核心问题: LLM/Agent 变强，很多时候不是因为模型结构变了，而是因为 instruction、prompt、数据选择、数据协议变好了。

代表论文:

1. [ChatInject: Abusing Chat Templates for Prompt Injection in LLM Agents](https://iclr.cc/virtual/2026/poster/10009048)
2. [Neuron-Aware Data Selection in Instruction Tuning for Large Language Models](https://iclr.cc/virtual/2026/poster/10006861)
3. [Prompt-MII: Meta-Learning Instruction Induction for LLMs](https://iclr.cc/virtual/2026/poster/10006473)
4. [Token-level Data Selection for Safe LLM Fine-tuning](https://iclr.cc/virtual/2026/poster/10007821)
5. [Data Selection for LLM Alignment Using Fine-Grained Preferences](https://iclr.cc/virtual/2026/poster/10007475)
6. [Explainable Token-level Noise Filtering for LLM Fine-tuning Datasets](https://iclr.cc/virtual/2026/poster/10009064)
7. [ASIDE: Architectural Separation of Instructions and Data in Language Models](https://iclr.cc/virtual/2026/poster/10010885)
8. [Holdout-Loss-Based Data Selection for LLM Finetuning via In-Context Learning](https://iclr.cc/virtual/2026/poster/10010818)
9. [Influence-Preserving Proxies for Gradient-Based Data Selection in LLM FineTuning](https://iclr.cc/virtual/2026/poster/10009699)
10. [Programming by Backprop: An Instruction is Worth 100 Examples When Finetuning LLMs](https://iclr.cc/virtual/2026/poster/10006605)
11. [Agent Data Protocol: Unifying Datasets for Diverse, Effective Fine-tuning of LLM Agents](https://iclr.cc/virtual/2026/poster/10006993)
12. [Inverse IFEval: Can LLMs Unlearn Stubborn Training Conventions to Follow Real Instructions?](https://iclr.cc/virtual/2026/poster/10007053)

阅读重点:

- Instruction/data selection 正在变成 post-training 的关键工程杠杆。
- Agent 数据需要统一协议，否则不同任务、工具、环境的数据很难复用。
- 指令与数据的边界本身是安全问题，ChatInject 和 ASIDE 值得放在一起读。
- Token-level 和 influence-based data selection 代表了更细粒度的数据治理方向。

## 子主题 7: Safety Risks for LLM Agents

核心问题: Agent 越会调用工具、越会自我改进，就越需要处理 prompt injection、jailbreak、backdoor、mis-evolution、strategic dishonesty 等风险。

代表论文:

1. [ChatInject: Abusing Chat Templates for Prompt Injection in LLM Agents](https://iclr.cc/virtual/2026/poster/10009048)
2. [Self-Jailbreaking: Language Models Can Reason Themselves Out of Safety Alignment After Benign Reasoning Training](https://iclr.cc/virtual/2026/poster/10008673)
3. [SafeDialBench: A Fine-Grained Safety Evaluation Benchmark for Large Language Models in Multi-Turn Dialogues with Diverse Jailbreak Attacks](https://iclr.cc/virtual/2026/poster/10010144)
4. [Reasoned Safety Alignment: Ensuring Jailbreak Defense via Answer-Then-Check](https://iclr.cc/virtual/2026/poster/10010790)
5. [AdvChain: Adversarial Chain-of-Thought Tuning for Robust Safety Alignment of Large Reasoning Models](https://iclr.cc/virtual/2026/poster/10007590)
6. [DualEdit: Mitigating Safety Fallback in LLM Backdoor Editing via Affirmation-Refusal Regulation](https://iclr.cc/virtual/2026/poster/10008415)
7. [Robust LLM Unlearning via Post Judgment and Multi-round Thinking](https://iclr.cc/virtual/2026/poster/10010525)
8. [Beyond Linear Probes: Dynamic Safety Monitoring for Language Models](https://iclr.cc/virtual/2026/poster/10011053)
9. [Invisible Safety Threat: Malicious Finetuning for LLM via Steganography](https://iclr.cc/virtual/2026/poster/10011363)
10. [Strategic Dishonesty Can Undermine AI Safety Evaluations of Frontier LLMs](https://iclr.cc/virtual/2026/poster/10010285)
11. [JailbreakLoRA: Your Downloaded LoRA from Sharing Platforms might be Unsafe](https://iclr.cc/virtual/2026/poster/10011545)
12. [ManagerBench: Evaluating the Safety-Pragmatism Trade-off in Autonomous LLMs](https://iclr.cc/virtual/2026/poster/10010089)
13. [Safety Instincts: LLMs Learn to Trust Their Internal Compass for Self-Defense](https://iclr.cc/virtual/2026/poster/10010033)
14. [Your Agent May Misevolve: Emergent Risks in Self-evolving LLM Agents](https://iclr.cc/virtual/2026/poster/10010580)

阅读重点:

- Reasoning training 可能让模型更会“绕过”安全对齐，Self-Jailbreaking 是一个非常重要的信号。
- Agent 场景下 prompt injection 不是普通 prompt 安全问题，而是工具链和上下文边界问题。
- 自我改进系统需要持续安全监控，否则可能出现 misevolution。
- LoRA、finetuning、steganography 这类供应链/微调风险值得单独关注。

## 推荐精读路线

### 路线 A: 最贴近 RSI / 自我改进

1. [R-Zero: Self-Evolving Reasoning LLM from Zero Data](https://iclr.cc/virtual/2026/poster/10011147)
2. [Test-Time Adaptation for LLM Agents via Environment Interaction](https://iclr.cc/virtual/2026/poster/10009800)
3. [EvoTest: Evolutionary Test-Time Learning for Self-Improving Agentic Systems](https://iclr.cc/virtual/2026/poster/10010217)
4. [ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory](https://iclr.cc/virtual/2026/poster/10007887)
5. [Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents](https://iclr.cc/virtual/2026/poster/10007327)
6. [Your Agent May Misevolve: Emergent Risks in Self-evolving LLM Agents](https://iclr.cc/virtual/2026/poster/10010580)

要看什么: 是否能形成“生成任务/经验 -> 验证 -> 更新策略/记忆 -> 更强 agent”的闭环，以及闭环失控的风险。

### 路线 B: Agent 工程能力

1. [MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent](https://iclr.cc/virtual/2026/poster/10007825)
2. [GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs](https://iclr.cc/virtual/2026/poster/10008792)
3. [In-the-Flow Agentic System Optimization for Effective Planning and Tool Use](https://iclr.cc/virtual/2026/poster/10009931)
4. [OrchestrationBench: LLM-Driven Agentic Planning and Tool Use in Multi-Domain Scenarios](https://iclr.cc/virtual/2026/poster/10009754)
5. [WALT: Web Agents that Learn Tools](https://iclr.cc/virtual/2026/poster/10008481)
6. [FlowSearcher: Synthesizing Memory-Guided Agentic Workflows for Web Information Seeking](https://iclr.cc/virtual/2026/poster/10011673)

要看什么: 记忆、工具、workflow、benchmark 如何一起决定 agent 表现。

### 路线 C: Post-training 与数据选择

1. [Prompt Curriculum Learning for Efficient LLM Post-Training](https://iclr.cc/virtual/2026/poster/10006420)
2. [Chasing the Tail: Effective Rubric-based Reward Modeling for Large Language Model Post-Training](https://iclr.cc/virtual/2026/poster/10007351)
3. [Data Selection for LLM Alignment Using Fine-Grained Preferences](https://iclr.cc/virtual/2026/poster/10007475)
4. [Towards Understanding Valuable Preference Data for Large Language Model Alignment](https://iclr.cc/virtual/2026/poster/10010595)
5. [Uni-DPO: A Unified Paradigm for Dynamic Preference Optimization of LLMs](https://iclr.cc/virtual/2026/poster/10010533)
6. [RiskPO: Risk-based Policy Optimization with Verifiable Reward for LLM Post-Training](https://iclr.cc/virtual/2026/poster/10010102)

要看什么: 未来 post-training 的胜负手可能在“数据/反馈质量”，而不是单纯更多 RL。

### 路线 D: Reasoning / CoT / Verifier

1. [FaithCoT-Bench: Benchmarking Instance-Level Faithfulness of Chain-of-Thought Reasoning](https://iclr.cc/virtual/2026/poster/10007686)
2. [Verifying Chain-of-Thought Reasoning via Its Computational Graph](https://iclr.cc/virtual/2026/poster/10010813)
3. [Are Reasoning LLMs Robust to Interventions on their Chain-of-Thought?](https://iclr.cc/virtual/2026/poster/10008704)
4. [Reinforcing General Reasoning Without Verifiers](https://iclr.cc/virtual/2026/poster/10007455)
5. [Quantile Advantage Estimation: Stabilizing RLVR for LLM Reasoning](https://iclr.cc/virtual/2026/poster/10009065)
6. [Pruning Long Chain-of-Thought of Large Reasoning Models via Small-Scale Preference Optimization](https://iclr.cc/virtual/2026/poster/10011162)

要看什么: reasoning 不只要强，还要可验证、可压缩、可监控。

### 路线 E: Agent 安全

1. [ChatInject: Abusing Chat Templates for Prompt Injection in LLM Agents](https://iclr.cc/virtual/2026/poster/10009048)
2. [Self-Jailbreaking: Language Models Can Reason Themselves Out of Safety Alignment After Benign Reasoning Training](https://iclr.cc/virtual/2026/poster/10008673)
3. [SafeDialBench: A Fine-Grained Safety Evaluation Benchmark for Large Language Models in Multi-Turn Dialogues with Diverse Jailbreak Attacks](https://iclr.cc/virtual/2026/poster/10010144)
4. [Beyond Linear Probes: Dynamic Safety Monitoring for Language Models](https://iclr.cc/virtual/2026/poster/10011053)
5. [Strategic Dishonesty Can Undermine AI Safety Evaluations of Frontier LLMs](https://iclr.cc/virtual/2026/poster/10010285)
6. [Your Agent May Misevolve: Emergent Risks in Self-evolving LLM Agents](https://iclr.cc/virtual/2026/poster/10010580)

要看什么: 自我改进 agent 的安全问题会从“输出有害内容”升级为“流程、工具、记忆、微调、评估被攻破”。

## 和 RSI Workshop 可合并阅读的主线

### 主线 1: Zero-data / Self-play / Self-evolving

- RSI Workshop: Agent0, Language Self-Play For Data-Free Training, R-Zero 类似方向
- ICLR 主会: R-Zero, SPELL, EvoTest, Darwin Gödel Machine

重点问题: 无人工数据或少人工数据时，模型如何自己生成任务、反馈和训练信号？

### 主线 2: Memory as self-improvement substrate

- RSI Workshop: SimpleMem, meta-learning agentic memory
- ICLR 主会: MemAgent, Look Back to Reason Forward, ReasoningBank, MemGen, GraphPlanner

重点问题: 自我改进到底是改参数，还是改记忆、经验库、workflow？

### 主线 3: Reliable verification loop

- RSI Workshop: code repair, adversarial unit tests, self-evolving rubrics
- ICLR 主会: ReVeal, FaithCoT-Bench, Verifying CoT, RiskPO

重点问题: 没有可靠验证，自我改进很容易变成自我确认。

### 主线 4: Safety of recursive/self-evolving agents

- RSI Workshop: reward hacking, SAHOO, TamperBench, agent misevolution
- ICLR 主会: ChatInject, Self-Jailbreaking, Dynamic Safety Monitoring, Strategic Dishonesty, Your Agent May Misevolve

重点问题: Agent 越自主，安全边界越应该放在整个闭环上，而不只是最后输出上。

