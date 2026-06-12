# 知识卡：KV Cache

## 资料来源

- 主笔记：[KV Cache 优化](../../src/04-推理优化/02-KV-Cache优化.md)
- 相关章节：[多头注意力变体](../../src/02-模型架构/04-多头注意力变体.md)
- 相关主题：自回归生成、Attention、Prefill、Decode、PagedAttention、GQA/MLA。

## 一句话结论

KV Cache 的本质不是“让 Attention 公式变快”，而是在自回归生成时缓存历史 token 的 Key 和 Value，避免每生成一个新 token 都重复计算历史上下文。

## 它解决什么问题

- 具体场景：LLM 推理时，模型一次生成一个 token，每个新 token 都要看前面已经生成的所有 token。
- 不用它时的问题：第 1 步算过的历史 token，在第 2、3、4 步还会被反复重新计算 K/V。
- 引入它后的变化：历史 token 的 K/V 只算一次，后续 decode 阶段只追加新 token 的 K/V。

## 前置知识

- 必须理解：自回归生成、Self-Attention、Q/K/V。
- 最好了解：Prefill/Decode、显存带宽、MHA/MQA/GQA、长上下文推理。

## 核心直觉

- 一句话直觉：KV Cache 像把读过的书签和笔记留下来，后面续写时不用重新把前文每一页都整理一遍。
- 类比：写文章时，你已经整理过前文重点，后面每写一句只需要把新句子的重点加入笔记。
- 类比边界：模型仍然要让新 token attend 到所有历史 K/V；KV Cache 省的是历史 K/V 的重复计算，不是完全跳过历史上下文。

## 最小例子

假设 prompt 是：

```text
我 喜欢
```

模型开始生成：

```text
我 喜欢 吃 面
```

没有 KV Cache：

```text
生成“吃”时：重新计算 我/喜欢 的 K/V
生成“面”时：重新计算 我/喜欢/吃 的 K/V
```

有 KV Cache：

```text
Prefill：一次性计算 我/喜欢 的 K/V，并存起来
Decode 1：只计算“吃”的 K/V，追加到 cache
Decode 2：只计算“面”的 K/V，追加到 cache
```

## 关键机制

1. 状态/对象：
   - K Cache：历史 token 的 Key。
   - V Cache：历史 token 的 Value。
   - 当前 Q：新 token 查询历史上下文时生成的 Query。
2. 过程/步骤：
   - Prefill 阶段并行处理 prompt，建立初始 KV Cache。
   - Decode 阶段每次只处理一个新 token。
   - 新 token 生成自己的 K/V，追加到 cache。
   - 当前 Q 和完整历史 K/V 做 Attention。
3. 成本/收益：
   - 收益：减少重复计算，提升长文本生成吞吐。
   - 成本：KV Cache 会随序列长度、层数、batch size 增长，占用大量显存。

## 工程应用

- 典型使用场景：聊天机器人、长文本生成、代码生成、多轮对话、长上下文问答。
- 影响的指标：首 token 延迟、decode 吞吐、显存占用、最大并发、最大上下文长度。
- 主要取舍：缓存越完整，重复计算越少；但序列越长、并发越高，显存压力越大。

## 常见误区

- 误区 1：KV Cache 缓存的是完整 Attention 结果。  
  正确理解：它缓存的是历史 token 的 K/V，不是最终输出。
- 误区 2：有了 KV Cache，Attention 就不用看历史 token 了。  
  正确理解：仍然要 attend 到历史 K/V，只是不再重复计算历史 K/V。
- 误区 3：KV Cache 只影响速度，不影响显存。  
  正确理解：KV Cache 是推理显存占用的重要来源，长上下文和高并发尤其明显。

## 边界和反例

- 什么时候不能简单收益：如果任务只做一次短 prompt 的分类或打分，KV Cache 的优势不明显。
- 什么时候容易误用：把 prefill 和 decode 混在一起讨论，误以为整个推理过程都不能并行。
- 一个反例：训练阶段通常可以并行处理完整序列，不是逐 token 生成，所以 KV Cache 不是训练加速的核心手段。

## 面试追问

- Q1：KV Cache 缓存的到底是什么，为什么不是 Q？
- Q2：Prefill 和 Decode 阶段的瓶颈分别是什么？
- Q3：为什么 GQA/MLA 能降低 KV Cache 显存？
- Q4：KV Cache 的显存占用怎么估算？
- Q5：PagedAttention 解决了 KV Cache 的什么工程问题？

## 内容转化角度

- 小红书：KV Cache 到底缓存了什么？
- 短视频：60 秒讲清楚为什么大模型生成越长越吃显存。
- 面试卡：KV Cache、Prefill、Decode、PagedAttention 一起怎么答。
- 长文：从 KV Cache 到长上下文推理优化。

## 迁移练习

- 同型：解释 Prefix Cache 和 KV Cache 的关系。
- 变式：比较 MHA、MQA、GQA 对 KV Cache 大小的影响。
- 不能用判断：训练 Transformer 时是否主要靠 KV Cache 加速？为什么？

