# FlashAttention 与 PagedAttention

> 目标：理解大模型推理优化中两个高频技术：FlashAttention 优化计算，PagedAttention 优化 KV Cache 内存管理。

## 一句话结论

FlashAttention 主要减少 Attention 计算中的显存读写，PagedAttention 主要减少 KV Cache 管理中的显存碎片。

## 1. Attention 的瓶颈

标准 Attention：

$$\text{Attention}(Q,K,V)=\text{softmax}(\frac{QK^T}{\sqrt{d}})V$$

瓶颈来自：

- 序列长度增加后 $QK^T$ 是 $n \times n$ 矩阵。
- 中间 attention matrix 显存占用大。
- GPU 计算快，但 HBM 读写很贵。

## 2. FlashAttention

FlashAttention 的核心思想：不要把完整 attention matrix 写回显存，而是在 SRAM 中分块计算 softmax 和输出。

直觉：

```text
传统 Attention:
QK^T -> 写显存 -> softmax -> 写显存 -> 乘 V

FlashAttention:
分块读 Q/K/V -> SRAM 内计算 -> 在线 softmax -> 输出
```

收益：

- 减少 HBM 访问。
- 降低中间激活显存占用。
- 长序列训练和推理更快。

需要注意：

- 它不改变 Attention 数学结果。
- 它不是降低理论 $O(n^2)$ 复杂度，而是优化 IO 和 kernel。
- 对硬件和实现依赖较强。

## 3. KV Cache 问题

自回归推理时，每个请求会不断增长 KV Cache：

```text
每层 KV Cache 大小 ≈ 2 * seq_len * num_kv_heads * head_dim * dtype_bytes
```

实际服务中，请求长度不同、生成长度不同，会导致显存碎片和调度困难。

## 4. PagedAttention

PagedAttention 借鉴操作系统分页思想，把 KV Cache 切成固定大小 block：

```text
逻辑 token 序列 -> block table -> 物理 KV block
```

优势：

- 减少连续大块显存分配。
- 支持不同请求共享和复用 block。
- 降低显存碎片。
- 便于 continuous batching。

## 5. Continuous Batching

传统 batching 要等一批请求一起完成，短请求会被长请求拖慢。

Continuous batching 允许：

- 新请求动态加入。
- 完成的请求及时退出。
- 每个 decoding step 重新组织 batch。

这能提升吞吐，但也要求 KV Cache 管理更灵活。

## 6. Prefix Cache

很多场景中 system prompt、工具说明、固定知识上下文是重复的。Prefix Cache 复用公共前缀的 KV：

适用场景：

- 固定 system prompt。
- Agent 工具定义。
- 多用户共享相同文档上下文。
- Few-shot 示例固定。

风险：

- 前缀必须 token 完全一致。
- 缓存命中率和业务 prompt 模板强相关。
- 隐私隔离要谨慎设计。

## 7. Speculative Decoding

投机解码使用小模型先草拟多个 token，再由大模型验证。

```text
draft model 生成候选 -> target model 并行验证 -> 接受一部分 token
```

适用：

- 大模型推理成本高。
- 小模型与大模型分布接近。
- 生成任务对延迟敏感。

限制：

- 实现复杂。
- draft model 质量影响接受率。
- 不一定适合所有采样策略。

## 面试追问

### Q1：FlashAttention 是否改变 Attention 复杂度？

回答：不改变理论 $O(n^2)$，它通过分块和 IO-aware 计算减少显存读写和中间矩阵存储，从而加速。

### Q2：PagedAttention 解决了什么问题？

回答：它解决服务场景中 KV Cache 动态增长和显存碎片问题，用分页式 block 管理 KV，使 continuous batching 更高效。

### Q3：Prefix Cache 和 KV Cache 是什么关系？

回答：KV Cache 是推理时缓存历史 K/V；Prefix Cache 是在多请求之间复用相同前缀的 KV Cache，提高命中时的首 token 延迟和吞吐。

## 内容选题

- 小红书：FlashAttention 和 PagedAttention 到底差在哪？
- 视频：vLLM 为什么能提升大模型吞吐？
- 面试：KV Cache 显存爆了怎么优化？
