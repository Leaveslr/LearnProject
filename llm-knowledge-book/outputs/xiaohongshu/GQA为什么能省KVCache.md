# 小红书图文笔记：GQA 为什么能省 KV Cache？

## 标题候选

- GQA 为什么能省 KV Cache？
- 大模型为什么不用完整 MHA？
- MHA、MQA、GQA、MLA 到底差在哪？
- KV Cache 太大，GQA 怎么救？
- LLaMA 为什么常用 GQA？

## 推荐标题

GQA 为什么能省 KV Cache？

## 封面文案

GQA 省在哪里

## 正文

讲 GQA，不能只说“分组注意力”。

它真正高频的面试点是：为什么能降低 KV Cache。

一句话结论：

> GQA 减少的是 KV 头数量，让多个 Query 头共享一组 K/V。

### 1. MHA 的问题

MHA 里，每个 Query 头都有独立 K/V。

如果有 32 个 Q 头，就可能有 32 组 KV。

推理时这些历史 KV 都要进 KV Cache。

### 2. MQA 怎么做？

MQA 更激进：

```text
所有 Q 头共享 1 组 K/V
```

很省，但表达可能受影响。

### 3. GQA 怎么折中？

GQA 把 Q 头分组：

```text
32 个 Q 头，8 个 KV 头
每 4 个 Q 头共享 1 组 KV
```

所以它比 MHA 省 KV Cache，又比 MQA 保留更多表达空间。

### 4. MLA 又是什么？

MLA 不只是减少 KV 头，而是把 KV 信息压缩成低维 latent，再需要时恢复。

它是更进一步的 KV 压缩思路。

## 面试回答卡

```text
KV Cache 大小和 KV head 数量强相关。
MHA 中每个 Q head 有自己的 K/V，缓存最大。
MQA 所有 Q head 共享一组 K/V，缓存最小但可能损失表达。
GQA 让多个 Q head 共享一组 K/V，
在质量和显存之间折中。
```

## 配图建议

- 图 1：MHA/MQA/GQA 三列对比。
- 图 2：32 Q 头、8 KV 头共享示意。
- 图 3：KV Cache 和 KV heads 关系。
- 图 4：MLA latent cache。

## 标签

#大模型 #LLM #GQA #KVCache #Transformer #AI面试

## 下一篇选题

MLA 和 GQA 到底有什么区别？

