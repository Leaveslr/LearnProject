# 流程走样例：Attention

## 目标

把 Attention 讲成“动态取上下文信息”的机制，而不是只背公式。

## 1. 问题场景

语言理解经常需要跨位置取信息。处理 `it` 时，需要知道它指代前面的哪个实体。

固定窗口和顺序模型不够直接，Attention 让每个位置可以直接看相关上下文。

## 2. 直觉模型

```text
Q：我想找什么
K：我能被怎么匹配
V：我提供什么内容
```

Attention 是“先匹配，再取内容”。

## 3. 最小例子

```text
The animal didn't cross the street because it was tired
```

处理 `it` 时，Q 会和所有 K 算相关性，最终从 `animal` 的 V 中拿更多信息。

## 4. 形式化

```text
Attention(Q,K,V)=softmax(QK^T/sqrt(d_k))V
```

步骤：

1. QK 相乘得到分数。
2. 缩放避免 softmax 饱和。
3. softmax 得到权重。
4. 加权 V 得到上下文表示。

## 5. Mask 和形态

- Encoder Self-Attention：双向看完整输入。
- Masked Self-Attention：只能看历史，不能偷看未来。
- Cross-Attention：一个序列向另一个序列取信息。

## 6. 易错点和反例

- 错误：Attention 权重就是解释。反例：权重高不一定是稳定因果解释。
- 错误：Decoder 训练必须逐 token。反例：训练有完整序列，可用 causal mask 并行算 loss。
- 错误：Attention 没有成本。反例：长上下文下注意力矩阵按长度二次增长。

## 7. 迁移练习

- 图文模型里的 Cross-Attention 是谁问谁？
- 为什么 causal mask 是下三角？
- 长上下文为什么需要 FlashAttention 或稀疏注意力？

