# Embedding 与向量相似度

## 一句话结论

Embedding 是把离散 token 变成连续向量的方式。只有变成向量，模型才能用矩阵计算处理文字、语义和上下文。

## 1. 为什么需要 Embedding

文本本来是离散符号：

```text
猫、狗、苹果、Transformer
```

神经网络不能直接理解这些字面符号，它需要数字。最简单的方法是给每个 token 一个编号，但编号没有语义：

```text
猫 = 12
狗 = 983
苹果 = 4
```

编号大小不代表任何语义关系。Embedding 的做法是：给每个 token 学一个向量。

```text
猫 -> [0.21, -0.33, 0.08, ...]
狗 -> [0.19, -0.29, 0.10, ...]
```

如果训练得好，语义相近的 token 会在向量空间里更接近。

## 2. Embedding 表到底是什么

Embedding 本质上是一个矩阵：

```text
词表大小 V = 100000
向量维度 d = 4096
Embedding 矩阵形状 = V x d
```

当输入 token id 是 `1234` 时，模型就从矩阵中取出第 1234 行，作为这个 token 的初始表示。

```text
token id -> 查表 -> token embedding
```

这一步不是手工设计语义，而是在训练中学出来的。

## 3. Token Embedding 和上下文表示的区别

初学者很容易把两者混在一起。

| 类型 | 含义 |
| --- | --- |
| Token Embedding | 某个 token 的静态初始向量 |
| Contextual Representation | 经过 Transformer 多层计算后，融合上下文的动态表示 |

例如“苹果”：

```text
我吃了一个苹果
我买了苹果公司的股票
```

刚进模型时，“苹果”的 token embedding 可能一样；经过上下文计算后，两句话里的表示会变得不同。

## 4. 向量相似度

常见相似度有：

- 点积。
- 余弦相似度。
- 欧氏距离。

RAG 和语义检索里最常见的是余弦相似度或点积。

余弦相似度关注方向是否接近：

```text
cos(a, b) = a · b / (|a| |b|)
```

直觉上，两个向量方向越一致，语义越可能接近。

## 5. Embedding 在 LLM 里的三种用法

### 5.1 输入 Embedding

用于把 token id 变成模型能处理的向量。

```text
token ids -> token embeddings -> Transformer blocks
```

### 5.2 输出 Embedding / lm_head

模型最后要把 hidden state 转回词表 logits：

```text
hidden state -> lm_head -> vocabulary logits
```

很多模型会做权重共享，让输入 embedding 和输出 lm_head 使用同一组权重。

### 5.3 语义 Embedding

RAG 里的 embedding 模型用于把 query 和文档 chunk 转成向量，再做相似度检索。

```text
query -> query vector
chunk -> chunk vector
相似度排序 -> top-k chunks
```

注意：RAG embedding 模型不一定等于生成用的 LLM。

## 6. 为什么 Embedding 会影响 RAG

RAG 的第一步是“找资料”。如果 embedding 模型不能把语义相近的问题和文档映射到相近位置，后面的生成模型再强也可能拿不到正确证据。

常见问题：

- 领域术语 embedding 不准。
- 中文和英文混合检索效果差。
- 短 query 信息太少。
- chunk 太长导致语义混杂。
- 相似但不相关的内容被召回。

## 7. 常见误区

### 误区一：Embedding 向量每一维都有明确含义

通常没有。单独某一维很难解释，语义更多分布在整个向量空间里。

### 误区二：向量相似就一定答案正确

不一定。向量相似只代表语义接近，不代表事实正确、时间最新或适合回答当前问题。

### 误区三：LLM 的 token embedding 就能直接拿来做 RAG

生成模型的内部表示和检索 embedding 的训练目标不同。生产 RAG 通常使用专门的 embedding 模型。

## 面试追问

### Q1：Embedding 为什么能表示语义？

因为训练过程中，相似上下文里的 token 会受到相似的梯度更新，长期训练后会在向量空间里形成结构化关系。

### Q2：Embedding 和 one-hot 有什么区别？

one-hot 是稀疏离散表示，维度等于词表大小，不能表达语义相似；embedding 是低维稠密表示，可以通过训练学习语义关系。

### Q3：RAG 里 embedding 模型怎么选？

看语言、领域、检索任务、向量维度、延迟、成本和评测结果。不能只看排行榜，最好用自己的 golden set 评估召回率。

## 学习检查

学完本章后，应该能独立讲清：

- token id 为什么不能直接作为模型输入。
- token embedding 和上下文表示有什么区别。
- 为什么 RAG 的 embedding 质量会影响最终答案。
