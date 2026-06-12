# 短视频脚本：KV Cache 到底缓存了什么？

## 选题

本期讲：KV Cache 到底缓存了什么，以及为什么它既能加速推理又会吃显存。

## 时长

建议 90-120 秒。

## 开头 0-5 秒

目标：纠正常见误区。

口播：

```text
很多人以为 KV Cache 缓存的是大模型生成过的答案，其实不是。它主要缓存的是历史 token 的 K 和 V。
```

画面：

```text
大字：KV Cache 不是缓存答案
小字：它缓存历史 K/V
```

## 第一段：问题背景 5-25 秒

口播：

```text
大模型生成文本时，不是一次性生成整段话，而是一个 token 一个 token 往外吐。
比如输入“我喜欢”，模型先生成“吃”，再生成“面”。
每生成一个新 token，都要参考前面的历史上下文。
如果每一步都重新计算历史 token 的 K/V，就会有大量重复计算。
```

画面：

```text
我 喜欢 -> 吃 -> 面
每一步都要看历史
```

## 第二段：核心机制 25-70 秒

口播：

```text
Attention 里有 Q、K、V。
Q 可以理解成：当前 token 想找什么信息。
K 是：历史 token 怎么被匹配。
V 是：历史 token 真正提供什么内容。

KV Cache 做的事就是：
历史 token 的 K 和 V 算过一次后，先存起来。
后面 decode 的时候，只计算新 token 的 K/V，再追加到缓存里。
当前 token 仍然会用自己的 Q，去和历史缓存的 K/V 做 Attention。
```

画面：

```text
Q：当前问题
K：历史索引
V：历史内容

新 token：只追加自己的 K/V
```

## 第三段：工程或面试视角 70-105 秒

口播：

```text
所以 KV Cache 的收益是减少重复计算，尤其适合长文本生成、多轮对话和代码生成。
但它不是免费的。
序列越长、层数越多、batch size 越大，KV Cache 占的显存就越多。
这也是为什么 GQA、MLA、PagedAttention 这些优化，经常和 KV Cache 一起出现。
```

画面：

```text
收益：少算历史 K/V
代价：更多显存
相关优化：GQA / MLA / PagedAttention
```

## 结尾 105-120 秒

口播：

```text
所以一句话记住：KV Cache 的本质不是缓存答案，而是复用历史 token 的 K/V。它省计算，但吃显存。
```

画面：

```text
KV Cache = 复用历史 K/V
省计算，但吃显存
```

## 可复用素材

- 对比表：无 KV Cache vs 有 KV Cache。
- 流程图：Prefill -> Decode -> 追加 K/V。
- 公式：`2 * seq_len * num_kv_heads * head_dim * dtype_bytes * layers * batch`。
- 例子：`我 喜欢 -> 吃 -> 面`。

