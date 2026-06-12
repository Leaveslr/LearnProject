# Transformer 高频问题索引

> 目标：把 Transformer 架构相关高频问题集中成一个复习入口。详细原理仍回到各专题笔记，本文件负责查漏补缺和面试快速串联。

## 1. Attention / QKV

### Q1: Q/K/V 分别是什么？为什么要拆成三套矩阵？

短答：Q 表示“我想找什么信息”，K 表示“我能被怎么匹配”，V 表示“我实际提供什么内容”。拆成三套矩阵可以让同一个 token 在查询、匹配、内容表达三个角色上学习不同表示。

详见：[注意力机制](./02-注意力机制.md)、[Transformer 详解](./01-Transformer详解.md)

### Q2: 为什么 Attention 要除以 `sqrt(d_k)`？

短答：当向量维度变大时，Q 和 K 的点积数值容易变大，softmax 会进入饱和区，梯度变小。除以 `sqrt(d_k)` 可以稳定注意力分数尺度。

详见：[注意力机制](./02-注意力机制.md)

### Q3: Self-Attention、Masked Self-Attention、Cross-Attention 有什么区别？

短答：

- Self-Attention：Q/K/V 都来自同一个序列。
- Masked Self-Attention：Self-Attention 加因果 mask，当前位置不能看未来。
- Cross-Attention：Q 来自当前序列，K/V 来自另一个序列，例如 Decoder 关注 Encoder 输出。

详见：[Transformer 详解](./01-Transformer详解.md)、[注意力机制](./02-注意力机制.md)

## 2. 多头注意力与 KV Cache

### Q4: 为什么要用 Multi-Head Attention？

短答：不同头可以在不同子空间关注不同关系，例如语法、指代、实体、位置等。多头不是简单重复，而是让模型从多个角度聚合上下文。

详见：[注意力机制](./02-注意力机制.md)

### Q5: MHA / MQA / GQA / MLA 有什么区别？

短答：

- MHA：每个 Q 头都有独立 K/V，表达强但 KV Cache 大。
- MQA：所有 Q 头共享一组 K/V，KV Cache 最小但可能损失表达。
- GQA：多个 Q 头共享一组 K/V，在质量和显存之间折中。
- MLA：用低秩潜变量压缩 K/V，进一步降低 KV Cache。

详见：[多头注意力变体](./04-多头注意力变体.md)、[KV Cache 优化](../04-推理优化/02-KV-Cache优化.md)

### Q6: GQA 为什么能减少推理显存？

短答：自回归推理要缓存历史 token 的 K/V。GQA 减少 KV 头数量，让多个 Q 头共享一组 K/V，所以 KV Cache 按 `num_kv_heads` 而不是 `num_q_heads` 增长。

详见：[多头注意力变体](./04-多头注意力变体.md)

## 3. 位置编码

### Q7: Transformer 为什么需要位置编码？

短答：Self-Attention 本身对 token 顺序不敏感。如果没有位置信息，“狗咬人”和“人咬狗”只是一组 token 的不同排列，模型难以区分顺序语义。

详见：[位置编码](./03-位置编码.md)

### Q8: RoPE 为什么适合大模型？

短答：RoPE 把位置信息注入 Q/K 的旋转中，使注意力分数天然包含相对位置信息。它比绝对位置编码更适合长上下文和长度外推，因此常见于 LLaMA、Qwen 等模型。

详见：[位置编码](./03-位置编码.md)

### Q9: ALiBi 和 RoPE 的区别？

短答：RoPE 通过旋转 Q/K 注入相对位置；ALiBi 直接在 attention score 上加和距离相关的线性 bias。ALiBi 外推简单，RoPE 表达能力和主流适配更强。

详见：[位置编码](./03-位置编码.md)

## 4. Decoder-only 与自回归生成

### Q10: 为什么现代 LLM 多采用 Decoder-only？

短答：LLM 的核心训练目标是 next token prediction，Decoder-only 的因果注意力天然匹配“看历史，预测未来”。结构简单，训练和推理路径一致，易于规模化。

详见：[Transformer 详解](./01-Transformer详解.md)

### Q11: 为什么训练时可以并行，推理时却要逐 token？

短答：训练时已知完整序列，可以用 causal mask 一次性并行计算每个位置预测下一个 token 的 loss；推理时未来 token 还没生成，只能生成一个 token 后再把它加入上下文继续生成。

详见：[Transformer 详解](./01-Transformer详解.md)、[KV Cache 优化](../04-推理优化/02-KV-Cache优化.md)

### Q12: Causal Mask 的作用是什么？

短答：防止当前位置看到未来 token，避免训练时信息泄露。没有 causal mask，模型会偷看答案，无法学习真实自回归生成。

详见：[Transformer 详解](./01-Transformer详解.md)

## 5. FFN / SwiGLU / Residual / Norm

### Q13: Attention 后为什么还要 FFN？

短答：Attention 负责 token 之间的信息交互，FFN 负责对每个 token 的表示做非线性加工。没有 FFN，模型主要是在做上下文加权，表达能力不足。

详见：[Transformer 详解](./01-Transformer详解.md)

### Q14: FFN 为什么通常先扩维再降维？

短答：扩维提供更大的中间特征空间，让模型有能力组合和筛选更复杂的模式；降维再回到 `d_model`，方便进入下一层 Transformer Block。

详见：[Transformer 详解](./01-Transformer详解.md)

### Q15: ReLU / GELU / SwiGLU 有什么区别？

短答：

- ReLU：简单截断负值。
- GELU：更平滑，早期 Transformer/ BERT/GPT 常见。
- SwiGLU：门控 FFN 变体，现代 LLM 常用，能让模型学习哪些通道应该通过。

详见：[Transformer 详解](./01-Transformer详解.md)

### Q16: BatchNorm / LayerNorm / RMSNorm 怎么选？

短答：CNN 常用 BatchNorm；Transformer 标准答案是 LayerNorm；现代 decoder-only LLM 常用 Pre-Norm + RMSNorm。原因是序列长度可变、自回归推理 batch 不稳定、分布式训练不希望同步 batch 统计量。

详见：[Transformer 详解](./01-Transformer详解.md)

### Q17: Residual Connection 为什么重要？

短答：残差连接提供一条稳定的信息和梯度通路，让深层 Transformer 更容易训练。可以理解为模型只需要学习“相对输入的增量”，而不是每层都从零重建表示。

详见：[Transformer 详解](./01-Transformer详解.md)

## 6. 推理优化与复杂度

### Q18: KV Cache 是什么？为什么能加速推理？

短答：自回归生成时，历史 token 的 K/V 每一步都会被用到。KV Cache 把历史 K/V 缓存起来，新 token 只计算自己的 Q/K/V，并复用历史 K/V，避免重复计算。

详见：[KV Cache 优化](../04-推理优化/02-KV-Cache优化.md)

### Q19: FlashAttention 优化了什么？

短答：FlashAttention 不改变 Attention 的理论 `O(n^2)` 复杂度，而是通过分块和 IO-aware 计算，避免完整 attention matrix 频繁读写 HBM，减少显存占用和内存带宽瓶颈。

详见：[FlashAttention 与 PagedAttention](../04-推理优化/03-FlashAttention与PagedAttention.md)

### Q20: 如果上下文长度翻倍，计算和显存怎么变化？

短答：标准 Attention 计算量大致按 `O(n^2)` 增长，长度翻倍，attention 计算约变成 4 倍；KV Cache 显存按 `O(n)` 增长，长度翻倍，KV Cache 约变成 2 倍。

详见：[注意力机制](./02-注意力机制.md)、[KV Cache 优化](../04-推理优化/02-KV-Cache优化.md)

### Q21: Transformer 的主要缺点是什么？

短答：

- 标准 Self-Attention 对长序列是 `O(n^2)`。
- 自回归推理无法完全并行生成。
- 长上下文下 KV Cache 显存压力大。
- 对位置信息没有天然建模，需要位置编码。
- 架构强但成本高，训练和推理都依赖高性能硬件。

## 7. 现代大模型结构

### Q22: LLaMA / Qwen / DeepSeek / GPT 这些模型结构差异看什么？

短答：主要看 Decoder-only 主体是否一致，以及位置编码、归一化、FFN 激活、注意力变体、MoE、上下文长度、推理优化等组件差异。

详见：[主流模型架构深度对比](../07-主流模型架构/01-主流模型架构深度对比.md)

### Q23: 为什么 RMSNorm、RoPE、SwiGLU、GQA 经常一起出现？

短答：它们分别服务于现代 LLM 的关键目标：RMSNorm 稳定且轻量，RoPE 支持相对位置和长上下文，SwiGLU 提升 FFN 表达，GQA 降低 KV Cache。组合起来适合大规模 decoder-only 模型。

详见：[Transformer 详解](./01-Transformer详解.md)、[位置编码](./03-位置编码.md)、[多头注意力变体](./04-多头注意力变体.md)

### Q24: MoE 和 Dense Transformer 的区别？

短答：Dense 模型每个 token 都经过同一套 FFN 参数；MoE 为每个 token 动态选择部分专家参与计算，在总参数量很大时保持较低活跃参数和计算成本。

详见：[MoE 详解](./06-MoE详解.md)

## 8. 手写 Transformer Block

面试中可以写一个简化版 Pre-Norm Decoder Block：

```python
class DecoderBlock(nn.Module):
    def __init__(self, d_model, attn, ffn, norm):
        super().__init__()
        self.attn = attn
        self.ffn = ffn
        self.norm1 = norm(d_model)
        self.norm2 = norm(d_model)

    def forward(self, x, causal_mask=None, kv_cache=None):
        x = x + self.attn(self.norm1(x), mask=causal_mask, kv_cache=kv_cache)
        x = x + self.ffn(self.norm2(x))
        return x
```

讲解顺序：

1. `norm1(x)`：先稳定输入尺度。
2. `attn(...)`：让当前 token 从上下文拿信息。
3. `x + ...`：残差保留原信息和梯度通路。
4. `norm2(x)`：进入 FFN 前再次稳定。
5. `ffn(...)`：每个 token 独立做非线性加工。
6. 再残差：输出给下一层。

## 9. 一句话总复习

Transformer 可以这样串起来：

> Token 先变成向量，加上位置信息；每层用 Attention 和上下文沟通，用 FFN 加工自身表示，用 Residual + Norm 稳定深层训练；现代 LLM 通常采用 Decoder-only、Causal Mask、RoPE、RMSNorm、SwiGLU、GQA/MLA，并通过 KV Cache 和 FlashAttention 优化推理。

