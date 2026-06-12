# 知识卡：MHA / MQA / GQA / MLA

## 资料来源

- 主笔记：[多头注意力机制变体详解](../../src/02-模型架构/04-多头注意力变体.md)

## 一句话结论

MHA、MQA、GQA、MLA 的核心差异，是 Query 头如何共享或压缩 Key/Value，从而在表达能力和 KV Cache 成本之间取舍。

## 它解决什么问题

- 标准 MHA 每个 Q 头都有独立 K/V，表达强但 KV Cache 大。
- 长上下文和高并发推理中，KV Cache 成为显存瓶颈。
- MQA/GQA/MLA 通过减少或压缩 KV 来降低推理成本。

## 核心直觉

- MHA：每个小组都有自己的资料库。
- MQA：所有小组共用一份资料库。
- GQA：几个小组共用一份资料库。
- MLA：先把资料压缩成低维笔记，需要时再展开。

## 最小例子

```text
32 个 Q 头
MHA：32 组 KV
MQA：1 组 KV
GQA：8 组 KV，每 4 个 Q 头共享 1 组 KV
MLA：缓存低维 latent，再动态恢复 K/V
```

## 关键机制

- KV Cache 大小和 `num_kv_heads` 强相关。
- MQA 把 `num_kv_heads` 降到 1。
- GQA 保留多个 KV 组，兼顾质量和显存。
- MLA 缓存低维潜变量，进一步压缩 KV 表示。

## 工程应用

- MHA：早期 Transformer、BERT/T5 等。
- MQA：极致省 KV，但质量可能受损。
- GQA：现代 LLM 常见折中。
- MLA：DeepSeek 系列代表，适合长上下文成本优化。

## 常见误区

- GQA 是为了提升训练效果，而不是推理显存。
- MQA 一定比 GQA 好。
- KV 头少等于 Q 头少。

## 边界和反例

- KV 共享太激进可能影响表达能力。
- 不同模型的具体实现和 head_dim 设计会影响实际收益。
- MLA 不是简单“少几个头”，而是低秩压缩和解压机制。

## 面试追问

- GQA 为什么能降低 KV Cache？
- MQA 和 GQA 的质量/成本取舍？
- MLA 和 GQA 的区别？

## 内容转化角度

- 小红书：为什么大模型不都用完整 MHA？
- 短视频：32 个 Q 头，KV 到底怎么共享？
- 面试卡：从 KV Cache 反推 GQA/MLA。

## 迁移练习

- 同型：计算 32 Q 头、8 KV 头的共享比例。
- 变式：长上下文服务为什么偏爱 GQA/MLA？
- 判断：GQA 会减少 Q 的头数吗？

