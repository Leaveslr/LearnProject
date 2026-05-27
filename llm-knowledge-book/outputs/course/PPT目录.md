# LLM 系统掌握课程 PPT 目录

> 目标：为后续制作正式课件提供 slide-level 结构。

## Deck 0：课程导论

1. 课程目标。
2. LLM 知识为什么容易碎。
3. 全链路学习地图。
4. 10 周学习路径。
5. 课程产出要求。

## Deck 1：基础原理与 Tokenizer

1. 文本为什么不能直接进模型。
2. token id 与 embedding。
3. 交叉熵和最大似然。
4. BPE 的直觉。
5. 中文 token 与成本。
6. 解码策略：temperature / top-k / top-p。
7. 练习：BPE 手算。

## Deck 2：Attention 与 Transformer

1. Transformer block 总览。
2. Q/K/V 直觉。
3. Scaled dot-product attention。
4. Causal mask。
5. FFN、Norm、Residual。
6. Decoder-only LLM。
7. 练习：画出 block。

## Deck 3：现代架构

1. 位置编码问题。
2. RoPE 直觉。
3. MHA / MQA / GQA / MLA。
4. KV Cache 与注意力变体。
5. MoE 与 router。
6. 主流模型架构对比。
7. 练习：GQA 显存对比。

## Deck 4：训练与数据工程

1. 预训练目标。
2. 数据来源。
3. 清洗、去重、配比。
4. benchmark contamination。
5. 分布式训练显存组成。
6. DP / TP / PP / ZeRO。
7. 练习：并行策略选择。

## Deck 5：SFT、微调与对齐

1. 预训练到助手模型。
2. SFT 数据格式。
3. loss masking。
4. LoRA / QLoRA。
5. RLHF / PPO。
6. DPO / GRPO。
7. 练习：微调方案设计。

## Deck 6：推理优化与部署

1. Prefill vs Decode。
2. KV Cache。
3. KV Cache 显存公式。
4. FlashAttention。
5. PagedAttention。
6. 量化部署。
7. TTFT / TPOT / throughput。
8. 练习：压测指标表。

## Deck 7：RAG 系统

1. RAG 总架构。
2. 文档解析和 chunk。
3. embedding 与向量库。
4. BM25 / vector / hybrid search。
5. rerank。
6. RAG eval。
7. 错误归因。
8. 练习：golden set 设计。

## Deck 8：Agent 工程

1. Workflow vs Agent。
2. ReAct。
3. tool schema。
4. memory 和 state。
5. HITL。
6. trace 和 observability。
7. Agent eval。
8. 练习：工具调用 trace。

## Deck 9：评估、安全与监控

1. LLM eval。
2. RAG eval。
3. Agent eval。
4. LLM-as-judge 风险。
5. prompt injection。
6. jailbreak。
7. RAG 文档投毒。
8. 工具调用安全。
9. 线上监控。

## Deck 10：项目表达与面试闭环

1. 面试为什么不只考定义。
2. 知识点到追问映射。
3. 项目表达模板。
4. baseline 和指标。
5. 失败案例复盘。
6. 毕业项目示例。
7. 最终复习路径。
