# Transformer Attention 机制讲解脚本

## 目标受众

完全没学过 Transformer，但听说过大模型的人。目标不是让观众背公式，而是让观众能用自己的话说出：Attention 为什么需要、Q/K/V 分别在做什么、公式每一段对应哪个动作。

## 参考讲解逻辑拆解

- 3Blue1Brown：先用具体词义例子建立“上下文会改变词向量”的动机，再把 Query、Key、Value 映射成可视化动作。
- Karpathy：每一步都让中间量可观察，避免“公式突然出现”。本视频用分数、权重、Value 流动来复用这个思路。
- 李宏毅：先给地图和学习者问题，再进入细节。本视频先问“词语如何读懂上下文”，再逐步引入术语。
- 原论文：Transformer 的核心是用注意力机制替代循环和卷积；Scaled Dot-Product Attention 可理解为匹配、归一化、加权求和。

资料来源：

- 3Blue1Brown attention transcript: https://pickscribe.com/v/eMlx5fFNoYc
- 3Blue1Brown transformer talk: https://www.3blue1brown.com/lessons/transformers-talk/
- Simon Willison 对 3Blue1Brown Attention 视频的评价和 Manim 工具说明: https://simonwillison.net/2024/Apr/11/3blue1brown/
- Attention Is All You Need: https://arxiv.org/abs/1706.03762
- 本项目讲解方法论: `teaching-algorithm-methods/abstracted-methods/knowledge-breakdown-framework.md`

## 成片节奏

预计时长约 1 分 49 秒。节奏设计为：

1. 0-22 秒：只讲问题和直觉，不出现公式。
2. 22-55 秒：引入 Q/K/V，用一个词义消歧例子走完整流程。
3. 55-78 秒：把分数、权重、Value 传递串起来，让公式有落点。
4. 78-103 秒：公式、多头、Mask、三句总结。

## 逐段字幕脚本

1. 一句话里的每个词，怎么知道自己真正的意思？这就是 Attention 要解决的问题。
2. 比如“苹果”这个词，单独看可能是水果；放到“苹果 手机 很 快”里，它更像是在说品牌。
3. 如果一个词只看自己，它就会迷路；如果它能看看周围的词，意思就会被上下文校准。
4. Self-Attention 的直觉是：每个词都向整句话发问，找出哪些词最值得参考。
5. Query 是“我想找什么线索”；Key 是“我能提供什么线索”；Value 是“真正要传过去的信息”。
6. “苹果”发出一个 Query：“我该怎么理解？”每个词拿出自己的 Key，和它做一次匹配打分。
7. 分数越高，说明这个词越有用。Softmax 会把分数变成一组加起来等于 1 的权重。
8. 然后用这些权重去加权 Value：手机的权重大，就把“品牌、设备”的信息更多传给苹果。
9. 于是原来模糊的“苹果”向量，被更新成“苹果手机”语境下的表示。
10. 公式 Attention(Q,K,V)=softmax(QK^T/sqrt(d_k))V，其实就是：匹配、归一化、加权求和。
11. 一个头可以看品牌关系，另一个头可以看修饰关系。多头注意力就是让模型同时学多种看法。
12. 在 GPT 这类模型里，预测下一个词时不能偷看未来，所以会用 Mask 把未来位置挡住。
13. 记住三件事：Attention 找相关词；Value 传递信息；多头让模型从多个角度理解上下文。
