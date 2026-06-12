# KV Cache 显存计算专题

## 一句话结论

KV Cache 用显存换推理速度。它避免重复计算历史 token 的 Key 和 Value，但上下文越长、batch 越大、层数越多，显存压力越大。

## 1. 为什么需要 KV Cache

自回归生成一次只生成一个 token。

没有 KV Cache 时，生成第 100 个 token 时，模型可能要重新计算前 99 个 token 的 K/V。

有 KV Cache 后：

```text
历史 token 的 K/V 存起来
新 token 只计算自己的 Q/K/V
再让新 token 的 Q 去 attend 历史 K/V
```

所以 KV Cache 主要节省 decode 阶段的重复计算。

## 2. Prefill 和 Decode

推理分两段：

| 阶段 | 做什么 | 特点 |
| --- | --- | --- |
| Prefill | 一次性处理 prompt | 计算密集，可并行 |
| Decode | 逐 token 生成回答 | 受 KV Cache、显存带宽和调度影响大 |

KV Cache 在 prefill 阶段被建立，在 decode 阶段不断增长。

## 3. KV Cache 存什么

每一层 Attention 都会产生 K 和 V。

对每个 token，每层都要存：

```text
Key 向量
Value 向量
```

所以显存和这些因素相关：

- batch size。
- sequence length。
- layer number。
- KV head number。
- head dimension。
- 数据类型字节数。

## 4. 基础计算公式

KV Cache 近似显存：

```text
KV Cache bytes =
batch_size
× seq_len
× num_layers
× 2
× num_kv_heads
× head_dim
× bytes_per_element
```

其中：

- `2` 表示 K 和 V 两份。
- `num_kv_heads` 是 K/V 头数，不一定等于 query heads。
- `bytes_per_element` 取决于精度，例如 FP16/BF16 通常是 2 bytes。

## 5. 例子：估算一个 32 层模型

假设：

```text
batch_size = 1
seq_len = 8192
num_layers = 32
num_kv_heads = 8
head_dim = 128
bytes_per_element = 2
```

则：

```text
1 × 8192 × 32 × 2 × 8 × 128 × 2
= 536870912 bytes
约 512 MB
```

这只是 batch size = 1 的 KV Cache。batch size 变成 16，就接近 8 GB。

## 6. MHA / MQA / GQA 对 KV Cache 的影响

假设 query heads = 32：

| 注意力类型 | KV 头数 | KV Cache |
| --- | --- | --- |
| MHA | 32 | 最大 |
| GQA | 例如 8 | 约为 MHA 的 1/4 |
| MQA | 1 | 最小 |

这就是为什么现代大模型推理常用 GQA/MQA：它们能显著降低 KV Cache 显存和带宽压力。

## 7. KV Cache 省了什么，没有省什么

KV Cache 节省：

- 历史 token 的 K/V 重复计算。
- decode 阶段大量重复前向计算。

KV Cache 不节省：

- 历史 K/V 本身的存储。
- 新 token 对历史 token 的 attention 读取。
- 长上下文带来的显存增长。

一句话：它让推理更快，但让显存更紧张。

## 8. 长上下文为什么贵

seq_len 是公式里的线性项：

```text
seq_len 翻倍 -> KV Cache 约翻倍
```

如果 batch size 同时变大，压力会更明显。

因此长上下文部署要同时关注：

- 最大输入长度。
- 最大输出长度。
- 并发请求数。
- prefix cache 命中率。
- 是否使用 GQA/MQA/MLA。
- KV cache quantization。

## 9. PagedAttention 解决什么

传统 KV Cache 可能要求连续显存块，面对不同长度请求时容易浪费。

PagedAttention 借鉴操作系统分页思想，把 KV Cache 切成块管理：

```text
逻辑上连续
物理上分页
```

它主要解决：

- 动态 batch 下显存碎片。
- 长短请求混合导致的浪费。
- 更高并发下的 KV Cache 管理。

## 10. Prefix Cache 解决什么

很多请求有相同前缀，例如：

- system prompt。
- 工具定义。
- 固定业务说明。
- 长文档公共开头。

Prefix Cache 会复用相同前缀的 KV Cache，减少重复 prefill。

它不改变单个 token 的 KV Cache 公式，但能降低重复请求的计算成本和首 token 延迟。

## 11. 常见误区

### 误区一：KV Cache 会降低显存

不对。KV Cache 通常增加显存占用，但减少重复计算，让 decode 更快。

### 误区二：上下文长度只影响计算，不影响显存

不对。KV Cache 和上下文长度近似线性相关，长上下文会显著增加显存压力。

### 误区三：FlashAttention 和 KV Cache 是一回事

不是。FlashAttention 优化 Attention 计算的 IO 和显存访问；KV Cache 是自回归推理时缓存历史 K/V。

## 面试追问

### Q1：KV Cache 显存怎么算？

用公式：

```text
batch_size × seq_len × num_layers × 2 × num_kv_heads × head_dim × bytes_per_element
```

其中 `2` 是 K 和 V。

### Q2：为什么 GQA 能减少 KV Cache？

因为 GQA 让多组 query heads 共享较少的 K/V heads，缓存的 K/V 头数减少，显存随之下降。

### Q3：PagedAttention 和 Prefix Cache 的区别？

PagedAttention 解决 KV Cache 的内存管理和碎片问题；Prefix Cache 复用相同前缀的计算结果，减少重复 prefill。

## 学习检查

学完本章后，应该能独立完成：

- 给定模型层数、KV 头数、head dim、上下文长度，估算 KV Cache 显存。
- 解释为什么 batch size 和长上下文会让推理显存快速上涨。
- 说明 GQA、PagedAttention、Prefix Cache 分别解决什么问题。
