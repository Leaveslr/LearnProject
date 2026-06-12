# 面试卡：KV Cache

## 高频问法

- KV Cache 是什么？缓存的到底是什么？
- 为什么推理时需要 KV Cache？
- Prefill 和 Decode 有什么区别？
- KV Cache 为什么会占显存？
- MQA/GQA/MLA 为什么能降低 KV Cache 压力？
- PagedAttention 解决了什么问题？

## 30 秒回答

KV Cache 是大模型自回归推理中的缓存机制，主要缓存历史 token 在每一层 Attention 里的 Key 和 Value。因为生成每个新 token 时都要 attend 到历史上下文，如果每一步都重新计算历史 token 的 K/V，会产生大量重复计算。KV Cache 会在 prefill 阶段建立 prompt 的 K/V，在 decode 阶段只追加新 token 的 K/V，从而提升生成效率。但它也会随序列长度、层数、batch size 增长，占用大量显存。

## 2 分钟回答

LLM 推理通常分成 prefill 和 decode 两个阶段。Prefill 阶段处理用户完整 prompt，可以并行计算，并建立第一批 KV Cache。Decode 阶段是自回归的，每次只能生成一个新 token。

在 Attention 里，每个 token 会产生 Q、K、V。生成新 token 时，当前 token 的 Q 需要和所有历史 token 的 K/V 做 Attention。如果没有 KV Cache，每一步都要重新计算所有历史 token 的 K/V。KV Cache 的做法是：历史 token 的 K/V 算过一次后就存起来，后续 decode 只计算新 token 的 K/V 并追加到 cache。

它的收益是减少重复计算，尤其适合长文本生成、多轮对话和高并发服务。代价是显存占用明显增加，近似和 `seq_len * num_layers * batch_size * num_kv_heads * head_dim` 成正比。所以现代模型会用 GQA、MLA，推理框架会用 PagedAttention、Prefix Cache 等方法降低 KV Cache 的显存和管理压力。

## 关键机制

- Prefill：并行处理完整 prompt，建立初始 K/V。
- Decode：逐 token 生成，每次追加新 token 的 K/V。
- Cache 对象：主要是历史 token 的 K 和 V。
- 主要收益：避免重复计算历史 K/V。
- 主要成本：长上下文和高并发下显存压力大。

## 面试官追问

### Q1：为什么不缓存 Q？

回答：历史 token 的 K/V 会被后续 token 反复使用，所以适合缓存。当前 token 的 Q 是每一步新生成 token 用来查询上下文的表示，主要服务当前这一步，不像历史 K/V 那样被后续所有步骤反复复用。

### Q2：Prefill 和 Decode 的瓶颈有什么不同？

回答：Prefill 处理完整 prompt，矩阵计算较多，但可以并行，常影响首 token 延迟。Decode 每次生成一个 token，自回归依赖强，难以并行，瓶颈常在 KV Cache 读取、显存带宽和调度管理。

### Q3：KV Cache 显存怎么估算？

回答：可以近似看成 `2 * seq_len * num_kv_heads * head_dim * dtype_bytes * num_layers * batch_size`。这里 `2` 是 K 和 V。实际还会受到框架布局、padding、分页管理和并发调度影响。

### Q4：为什么 GQA 能减少 KV Cache？

回答：KV Cache 大小和 `num_kv_heads` 直接相关。MHA 中每个 Q 头通常对应自己的 K/V 头，KV 头多；GQA 让多组 Q 头共享较少的 K/V 头，所以能在质量和显存之间折中。

### Q5：PagedAttention 解决了什么？

回答：PagedAttention 主要解决 KV Cache 连续显存分配、预留浪费和碎片问题。它把 KV Cache 切成固定大小的 block，像操作系统分页一样动态管理，从而提高显存利用率和并发能力。

## 容易翻车的回答

- 错误说法：KV Cache 缓存 Attention 输出。  
  正确说法：主要缓存历史 token 的 Key 和 Value。
- 错误说法：KV Cache 让模型不用看历史。  
  正确说法：模型仍然看历史，只是历史 K/V 不重复计算。
- 错误说法：KV Cache 只提升速度，没有代价。  
  正确说法：它减少计算，但增加显存占用和缓存管理复杂度。

## 工程延展

- 线上指标：TTFT、TPOT、吞吐、显存占用、最大并发、上下文长度。
- 系统瓶颈：Decode 阶段串行依赖、KV Cache 读写、显存带宽、碎片管理。
- 优化方向：GQA/MLA、PagedAttention、Prefix Cache、Continuous Batching、量化 KV Cache。

