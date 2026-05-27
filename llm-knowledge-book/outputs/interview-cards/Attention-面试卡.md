# 面试卡：Attention

## 高频问法

- Attention 的 Q/K/V 怎么理解？
- 为什么要除以 `sqrt(d_k)`？
- Masked Self-Attention 和 Cross-Attention 有什么区别？

## 30 秒回答

Attention 让每个 token 根据内容动态从上下文取信息。Q 表示当前 token 想找什么，K 表示其他 token 如何被匹配，V 表示真正提供的内容。公式是 `softmax(QK^T/sqrt(d_k))V`，先算相关性，再归一化成权重，最后加权求和 V。

## 2 分钟回答

Attention 的流程是：Q 和 K 做点积得到相关性分数，除以 `sqrt(d_k)` 防止维度大时分数过大导致 softmax 饱和，然后 softmax 得到权重，用权重加权 V 得到上下文表示。Encoder Self-Attention 可以双向看完整输入，Decoder 的 Masked Self-Attention 只能看历史，Cross-Attention 则是一个序列用 Q 去读另一个序列的 K/V。

## 追问

### Q1：为什么缩放？

回答：`d_k` 大时点积方差变大，softmax 容易饱和，梯度变小；除以 `sqrt(d_k)` 稳定数值。

### Q2：Attention 为什么能并行？

回答：训练时完整序列已知，可以一次性计算所有位置的 Q/K/V 和 mask 后的注意力。

### Q3：Attention 权重能解释模型吗？

回答：只能作为参考，不等于可靠因果解释。

## 容易翻车

- 错误：Q/K/V 是人工写死的语义。
- 正确：它们是输入经过可学习线性变换得到的表示。

