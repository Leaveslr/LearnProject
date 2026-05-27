# 知识卡：Attention

## 资料来源

- 主笔记：[注意力机制深度剖析](../../src/02-模型架构/02-注意力机制.md)

## 一句话结论

Attention 的本质是让每个 token 根据内容动态选择该从上下文哪些位置拿信息。

## 它解决什么问题

- RNN 难以高效建模长距离依赖。
- 固定窗口看不到全局上下文。
- Attention 让每个位置直接和所有相关位置交互，并且可以并行计算。

## 核心直觉

- Q：我想找什么。
- K：我能被怎么匹配。
- V：我真正提供什么内容。
- Attention：用 Q 和 K 算相关性，再用相关性加权 V。

## 最小例子

句子：

```text
The animal didn't cross the street because it was tired
```

处理 `it` 时，Attention 需要让它更多关注 `animal`，才能知道 `it` 指谁。

## 关键机制

```text
Attention(Q,K,V)=softmax(QK^T/sqrt(d_k))V
```

1. QK 相乘得到相关性分数。
2. 除以 `sqrt(d_k)` 防止数值过大导致 softmax 饱和。
3. softmax 得到权重。
4. 权重加权 V 得到上下文表示。

## 工程应用

- Self-Attention：同一序列内部交互。
- Masked Self-Attention：自回归模型不能看未来。
- Cross-Attention：一个序列读取另一个序列的信息。
- 长上下文下计算和显存压力会随长度快速增长。

## 常见误区

- Attention 权重等于完整解释性。
- Q/K/V 是人工定义的语义字段。
- Decoder 训练时也必须逐 token 串行计算。

## 边界和反例

- Attention 能直接看全局，但计算量随序列长度按二次增长。
- Causal mask 下不能看未来，否则会泄漏答案。
- 权重高不一定代表人类可解释的因果关系。

## 面试追问

- 为什么除以 `sqrt(d_k)`？
- Masked Self-Attention 和 Encoder Self-Attention 区别？
- Attention 为什么能并行？

## 内容转化角度

- 小红书：Q/K/V 到底怎么理解。
- 短视频：用“提问-匹配-取内容”讲 Attention。
- 面试卡：公式、mask、复杂度一起答。

## 迁移练习

- 同型：解释 Cross-Attention 在图文模型中的作用。
- 变式：为什么长上下文成本高？
- 判断：Attention 权重能直接当解释吗？

