# 流程走样例：MHA / MQA / GQA / MLA

## 目标

从 KV Cache 成本出发，讲清多头注意力变体为什么存在。

## 1. 问题场景

MHA 表达能力强，但每个 Q 头都有独立 K/V。推理时历史 K/V 要缓存，长上下文下显存压力大。

## 2. 直觉模型

- MHA：每个小组一份资料。
- MQA：所有小组共用一份资料。
- GQA：几个小组共用一份资料。
- MLA：先压缩成低维笔记，需要时再展开。

## 3. 最小例子

```text
32 个 Q 头
MHA: 32 组 KV
MQA: 1 组 KV
GQA: 8 组 KV
MLA: 缓存低维 latent
```

## 4. 机制拆解

KV Cache 近似正比于 `num_kv_heads`。

- MHA：`num_kv_heads = num_q_heads`。
- MQA：`num_kv_heads = 1`。
- GQA：`1 < num_kv_heads < num_q_heads`。
- MLA：不直接缓存完整 KV，而缓存压缩 latent。

## 5. 工程取舍

- MQA 最省，但可能牺牲表达。
- GQA 是现代 LLM 常见折中。
- MLA 更进一步压缩，但实现复杂。

## 6. 易错点和反例

- 错误：GQA 减少 Q 头。实际是减少 KV 头。
- 错误：MQA 一定最好。极致共享可能影响质量。
- 错误：MLA 就是 GQA 换名字。MLA 关键是低秩压缩缓存。

## 7. 迁移练习

- 32 Q 头、8 KV 头，每几个 Q 头共享一组 KV？
- 为什么长上下文模型更关心 KV 头数？
- GQA 和 KV Cache 公式怎么对应？

