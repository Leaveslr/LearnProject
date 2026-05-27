# 流程走样例：KV Cache

## 目标

用知识讲解方法论验证一个 LLM 工程知识点如何从学习笔记变成可讲内容。

知识点：KV Cache。

受众：正在准备大模型算法/工程面试的初学者。

## 1. 问题场景

大模型生成文本不是一次吐出整段话，而是一个 token 一个 token 地生成。

例如：

```text
用户输入：我喜欢
模型生成：吃 -> 面
```

不用 KV Cache 时，每生成一个新 token，模型都要重新处理前面所有 token 的 K/V。

瓶颈：

- 历史 token 被重复计算。
- 生成越长，重复越多。
- 多用户并发时，显存和带宽压力更大。

讲解句式：

> KV Cache 要解决的不是“模型不会算”，而是“同一段历史上下文被反复算”。

## 2. 已有经验

类比：

写文章时，你不会每写一句都重新整理一遍前文所有提纲，而是保留前面已经整理好的笔记，然后把新句子的重点追加进去。

类比边界：

- 你仍然要参考前文笔记。
- 你省掉的是“重新整理前文”的动作。
- 这对应 KV Cache 省掉历史 K/V 的重复计算，但当前 token 仍然要 attend 到历史 K/V。

诊断问题：

> KV Cache 省掉的是看历史上下文，还是省掉历史 K/V 的重复计算？

如果答成“省掉看历史”，说明对 Attention 过程理解错了。

## 3. 直觉模型

核心直觉：

KV Cache 是给历史 token 建一个可复用的 K/V 记忆表。

核心状态：

- 当前 token 的 Q：这一步要找什么信息。
- 历史 token 的 K：历史信息如何被匹配。
- 历史 token 的 V：历史信息真正提供什么内容。
- KV Cache：已经算好的历史 K/V。

讲解句式：

> 当前 token 仍然会提问，历史 token 仍然会回答；KV Cache 只是让历史 token 不用每一轮重新准备答案。

## 4. 最小流程演示

输入：

```text
我 喜欢
```

生成：

```text
吃 面
```

| 阶段 | 当前输入 | 没有 KV Cache | 有 KV Cache |
| --- | --- | --- | --- |
| Prefill | 我 喜欢 | 计算“我/喜欢”的 K/V | 计算并缓存“我/喜欢”的 K/V |
| Decode 1 | 吃 | 重新计算“我/喜欢/吃”的 K/V | 只计算“吃”的 K/V，追加 cache |
| Decode 2 | 面 | 重新计算“我/喜欢/吃/面”的 K/V | 只计算“面”的 K/V，追加 cache |

阶段总结：

> Prefill 像读完题目并建立笔记；Decode 像每写一个新字，就把这个新字的笔记追加进去。

## 5. 最小形式化

自然语言规则：

1. 对 prompt 做 prefill，计算所有 prompt token 的 K/V。
2. 把每层的 K/V 存进 cache。
3. decode 时，每次只输入最新 token。
4. 新 token 生成自己的 Q/K/V。
5. 新 K/V 追加到 cache。
6. 当前 Q 和完整 cache 中的 K/V 做 Attention。

伪代码：

```python
k_cache, v_cache = [], []

# prefill
k_prompt, v_prompt = compute_kv(prompt_tokens)
k_cache.extend(k_prompt)
v_cache.extend(v_prompt)

# decode
for token in generated_tokens:
    q_new = compute_q(token)
    k_new, v_new = compute_kv(token)
    k_cache.append(k_new)
    v_cache.append(v_new)
    output = attention(q_new, k_cache, v_cache)
```

## 6. 工程成本和收益

收益：

- 历史 K/V 不重复计算。
- Decode 阶段更高效。
- 长文本生成和多轮对话收益明显。

成本：

- Cache 随序列长度增长。
- 每层都要存 K/V。
- batch size 越大，显存压力越大。

估算公式：

```text
每层 KV Cache ≈ 2 * seq_len * num_kv_heads * head_dim * dtype_bytes
全模型 KV Cache ≈ 每层 KV Cache * num_layers * batch_size
```

这里的 `2` 是 K 和 V。

## 7. 正确性和效率解释

为什么可以缓存？

- 历史 token 的 K/V 在生成后续 token 时不会改变。
- 后续 token 只需要新增自己的 K/V。
- 当前 token 的 Q 会变化，所以 Q 不适合像历史 K/V 一样复用。

为什么会更快？

- 没有 KV Cache：每步重复计算历史 K/V。
- 有 KV Cache：每步只计算新 token 的 K/V。
- 长文本时，省掉的重复计算越来越多。

## 8. 易错点和反例

易错点：

- 把 KV Cache 说成缓存 Q/K/V。更准确地说，推理中主要缓存历史 K/V。
- 把 KV Cache 说成“不用 Attention”。实际上仍然要 Attention，只是 K/V 来源变成 cache。
- 只讲速度，不讲显存。KV Cache 是长上下文显存压力的重要来源。

反例：

如果任务是一次性处理短文本分类，不需要长时间自回归生成，那么 KV Cache 的价值就不明显。

边界：

训练时通常并行处理完整序列，不是逐 token decode，所以不要把 KV Cache 当成训练加速的核心解释。

## 9. 迁移练习

同型练习：

- Prefix Cache 和 KV Cache 分别缓存什么？有什么关系？

变式练习：

- 为什么 MQA/GQA 可以减少 KV Cache 显存？

边界判断：

- “KV Cache 能让模型不用看前文，所以生成更快。”这句话对不对？为什么？

## 10. 对框架的验证结论

KV Cache 这类工程知识不能只按“定义 -> 公式 -> 框架名”讲。更好的路径是：

```text
生成方式 -> 重复计算问题 -> 缓存直觉 -> prefill/decode 流程 -> 显存公式 -> 工程取舍 -> 面试追问
```

和算法知识相比，它更需要提前讲清“收益和成本同时存在”：KV Cache 省计算，但吃显存。

