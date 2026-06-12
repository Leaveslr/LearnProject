# LLM 知识点内容选题库

> 目标：把学习笔记转化成小红书图文、短视频和面试卡片的选题池。

## 使用方式

每学完一个知识点，至少补充：

- 一个小红书标题。
- 一个短视频标题。
- 一个面试追问。
- 一个适合配图的结构。

## 系列一：基础知识

| 知识点 | 小红书标题 | 视频标题 | 面试追问 |
| --- | --- | --- | --- |
| 交叉熵 | 大模型训练为什么还是交叉熵？ | 60 秒讲清楚 next token prediction | 交叉熵和最大似然什么关系？ |
| LayerNorm | Transformer 为什么不用 BatchNorm？ | LayerNorm 到底归一化了什么？ | LayerNorm 和 RMSNorm 区别？ |
| Tokenizer | Token 不等于词，别再理解错了 | BPE 是怎么切词的？ | Tokenizer 对 RAG 有什么影响？ |
| Embedding | Embedding 到底学到了什么？ | 文本如何变成向量？ | token embedding 和 hidden state 区别？ |

## 系列二：模型架构

| 知识点 | 小红书标题 | 视频标题 | 面试追问 |
| --- | --- | --- | --- |
| Attention | Attention 到底在算什么？ | Q/K/V 用一个例子讲明白 | 为什么除以 sqrt(d)？ |
| RoPE | RoPE 为什么适合大模型？ | 旋转位置编码直觉解释 | RoPE 如何表达相对位置？ |
| GQA | 为什么大模型不用完整 MHA？ | MHA/MQA/GQA 差在哪？ | GQA 怎么减少 KV Cache？ |
| MoE | MoE 为什么参数多但推理不爆炸？ | 专家模型如何路由？ | MoE 的负载均衡怎么做？ |

## 系列三：训练与对齐

| 知识点 | 小红书标题 | 视频标题 | 面试追问 |
| --- | --- | --- | --- |
| SFT | SFT 不是 LoRA，别混了 | 指令微调如何让模型听话？ | SFT 数据怎么构造？ |
| LoRA | LoRA 为什么只训练小矩阵？ | 低秩适配直觉解释 | rank 怎么选？ |
| DPO | DPO 为什么不需要奖励模型？ | 偏好对齐最小闭环 | DPO 和 PPO 区别？ |
| GRPO | GRPO 为什么适合推理模型训练？ | 组内相对优势怎么来？ | GRPO 省掉了什么？ |

## 系列四：推理部署

| 知识点 | 小红书标题 | 视频标题 | 面试追问 |
| --- | --- | --- | --- |
| KV Cache | KV Cache 到底缓存了什么？ | 为什么推理离不开 KV Cache？ | KV Cache 显存怎么算？ |
| FlashAttention | FlashAttention 不是改公式 | IO-aware Attention 直觉解释 | 它是否改变复杂度？ |
| PagedAttention | vLLM 为什么吞吐高？ | KV Cache 也能分页？ | PagedAttention 解决什么？ |
| 量化 | INT4、INT8、NF4 怎么选？ | 量化为什么会掉点？ | GPTQ 和 AWQ 区别？ |

## 系列五：RAG 与 Agent

| 知识点 | 小红书标题 | 视频标题 | 面试追问 |
| --- | --- | --- | --- |
| Chunk | RAG 分块不是越大越好 | chunk size 怎么定？ | 如何定位分块导致的错误？ |
| Hybrid Search | 向量检索为什么还要 BM25？ | 混合检索解决什么问题？ | rerank 放在哪一层？ |
| Agent | Agent 不是套壳 ChatGPT | workflow 和 agent 差在哪？ | Agent 如何防止死循环？ |
| Memory | Agent 记忆不是长上下文 | 长期记忆如何设计？ | 记忆召回错误怎么办？ |

## 系列六：评估与安全

| 知识点 | 小红书标题 | 视频标题 | 面试追问 |
| --- | --- | --- | --- |
| RAG Eval | RAG 错了该怪谁？ | 三层评估定位 RAG 问题 | Recall@k 和 Faithfulness 区别？ |
| Agent Eval | Agent 要看 trace，不只看答案 | 如何评估工具调用？ | Agent 成功率怎么定义？ |
| LLM-as-judge | 用模型评模型靠谱吗？ | Judge 模型有哪些偏见？ | 如何校准 LLM 评审？ |
| Prompt Injection | RAG 也会被注入攻击 | 文档里的恶意指令怎么办？ | 如何做安全边界？ |
