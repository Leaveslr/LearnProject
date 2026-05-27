# 小红书图文笔记：KV Cache 到底缓存了什么？

## 标题候选

- KV Cache 到底缓存了什么？
- 大模型推理为什么越聊越吃显存？
- 别再把 KV Cache 理解成缓存答案了
- 面试必问：Prefill 和 Decode 怎么讲？
- 一句话讲清楚 KV Cache
- KV Cache 不是让模型忘掉前文
- 为什么 GQA 能省 KV Cache？
- 长上下文推理的显存大头：KV Cache

## 推荐标题

KV Cache 到底缓存了什么？

## 封面文案

KV Cache 缓存了什么

## 正文

很多人第一次听 KV Cache，会以为它是在缓存模型生成过的“答案”。

其实不是。

一句话结论：

> KV Cache 主要缓存历史 token 的 Key 和 Value，避免自回归生成时反复计算历史上下文。

### 1. 为什么需要它？

大模型生成文本时，通常是一个 token 一个 token 往外吐。

比如：

```text
我 喜欢 -> 吃 -> 面
```

生成“吃”时，要看前面的“我、喜欢”。  
生成“面”时，又要看“我、喜欢、吃”。

如果每一步都重新计算所有历史 token 的 K/V，就会产生大量重复计算。

KV Cache 解决的就是这件事。

### 2. 它到底缓存什么？

Attention 里常见三个东西：

- Q：当前 token 想找什么信息
- K：历史 token 怎么被匹配
- V：历史 token 真正提供什么内容

KV Cache 缓存的是历史 token 的 K 和 V。

直觉上：

```text
历史 token 已经准备好的“索引”和“内容”，不用每轮重新准备。
```

当前 token 仍然会用自己的 Q 去查这些历史 K/V。

### 3. Prefill 和 Decode 怎么理解？

推理可以粗略分成两段：

```text
Prefill：读完 prompt，建立第一批 KV Cache
Decode：每生成一个 token，只追加这个 token 的 K/V
```

Prefill 像先读题。  
Decode 像一边写答案，一边把新写内容加入笔记。

### 4. 它为什么也会带来问题？

KV Cache 省了重复计算，但不是免费午餐。

它会占显存，而且长度越长越大。

近似可以这么理解：

```text
KV Cache 大小和
序列长度 * 层数 * batch size * KV 头数量
强相关
```

所以长上下文、多轮对话、高并发服务里，KV Cache 很容易成为显存大头。

### 5. 常见误区

误区 1：KV Cache 缓存的是完整 Attention 结果。  
正确理解：主要缓存历史 K/V。

误区 2：有 KV Cache 就不用看前文。  
正确理解：仍然要看前文，只是不重复算前文 K/V。

误区 3：KV Cache 只提升速度。  
正确理解：它减少计算，但增加显存和管理复杂度。

## 面试回答卡

如果面试官问：KV Cache 是什么？

可以这样答：

```text
KV Cache 是大模型自回归推理中的缓存机制。
它主要缓存历史 token 在每一层 Attention 中的 Key 和 Value。

这样 decode 阶段每生成一个新 token 时，
只需要计算新 token 的 K/V，
再让当前 Q 和历史缓存的 K/V 做 Attention，
避免重复计算历史上下文。

它能提升生成效率，
但会随着序列长度、层数、batch size 和 KV 头数量增加而占用更多显存。
```

## 配图建议

### 图 1：封面卡

```text
KV Cache 缓存了什么？
不是答案，是历史 K/V
```

### 图 2：无缓存 vs 有缓存

```text
无 KV Cache：
每一步重新算历史 K/V

有 KV Cache：
历史 K/V 复用，只追加新 token
```

### 图 3：Prefill / Decode 对比表

| 阶段 | 做什么 | 瓶颈 |
| --- | --- | --- |
| Prefill | 处理完整 prompt | 首 token 延迟 |
| Decode | 逐 token 生成 | KV Cache 读写和显存 |

### 图 4：误区卡

```text
KV Cache 不是跳过历史
而是复用历史 K/V
```

## 标签

#大模型 #LLM #KVCache #AI面试 #推理优化 #Transformer #算法岗

## 下一篇选题

下一篇可以继续拆：为什么 GQA/MLA 能降低 KV Cache 显存？

