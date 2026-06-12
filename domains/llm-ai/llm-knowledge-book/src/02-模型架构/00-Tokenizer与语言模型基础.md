# Tokenizer 与语言模型基础

> 目标：理解文本如何变成 token，以及 next token prediction 如何支撑 LLM 的训练和生成。

## 一句话结论

Tokenizer 决定了模型看到的基本单位，语言模型则学习在上下文条件下预测下一个 token。

## 1. 为什么需要 Tokenizer

神经网络不能直接处理自然语言字符串，需要把文本转换成整数 token id：

```text
文本 -> token -> token id -> embedding -> 模型
```

Tokenizer 的好坏会影响：

- 序列长度。
- 多语言表现。
- 代码和特殊符号处理。
- OOV 问题。
- 推理成本。

## 2. 常见分词方式

### Word-level

按词切分，直观但词表巨大，遇到新词容易 OOV。

### Character-level

按字符切分，词表小但序列变长，长距离建模压力大。

### Subword-level

现代 LLM 常用子词分词，在词表大小和序列长度之间折中。

常见算法：

- BPE：从字符开始合并高频片段。
- WordPiece：常见于 BERT 系列。
- SentencePiece：把文本当作 unicode 字符序列处理，适合多语言。

## 3. BPE 直觉

BPE 的核心是反复合并语料中最常见的相邻 token：

```text
l o w
l o w e r
n e w e s t

合并高频 pair 后：
low er
new est
```

优点：

- 常见词可以用较少 token 表示。
- 生僻词可以拆成子词。
- 词表大小可控。

## 4. 特殊 Token

常见特殊 token：

- BOS：序列开始。
- EOS：序列结束。
- PAD：padding。
- UNK：未知 token。
- system/user/assistant：对话角色标记。
- image/audio/tool：多模态或工具调用标记。

面试要点：chat template 本质上也是把对话结构序列化成模型能理解的 token 序列。

## 5. Next Token Prediction

自回归语言模型训练目标：

```text
输入：x1, x2, ..., x(t-1)
目标：预测 xt
```

训练时一次性并行计算所有位置的 loss，推理时逐 token 生成。

关键差异：

| 阶段 | 输入 | 计算方式 | 是否并行 |
| --- | --- | --- | --- |
| 训练 | 完整序列 | teacher forcing | 序列内并行 |
| 推理 | 历史生成 token | autoregressive decoding | 逐 token |

## 6. 采样策略

模型输出 logits，经过 softmax 得到概率分布。生成时需要采样策略：

- Greedy：每次选最大概率 token，稳定但可能单调。
- Beam Search：保留多个候选，适合翻译等任务，不一定适合开放生成。
- Temperature：控制分布平滑程度。
- Top-k：只从前 k 个 token 采样。
- Top-p：从累计概率达到 p 的 token 集合采样。

## 7. Tokenizer 的工程影响

### 序列长度

同一段文本，不同 tokenizer 的 token 数可能不同。token 数越多，训练和推理成本越高。

### 多语言

英文优化的 tokenizer 可能让中文被切得更碎，导致上下文浪费。

### 代码

代码中缩进、符号、长变量名会影响 tokenization，进而影响代码模型效果。

### 安全

特殊字符、unicode 变体、不可见字符可能绕过规则或安全检测。

## 常见误区

- **误区 1：token 等于中文词或英文单词。** 实际 token 可能是字符、子词、空格片段或特殊符号。
- **误区 2：词表越大越好。** 词表大能减少序列长度，但 embedding 和输出层参数也更大。
- **误区 3：训练和推理都是逐 token 计算。** 训练可以并行计算所有位置的损失，推理通常必须自回归逐步生成。

## 面试追问

### Q1：BPE 为什么能解决 OOV？

回答：BPE 保留子词和字符级 fallback，生僻词可以拆成已知子词，而不是直接变成 unknown。

### Q2：为什么推理比训练更依赖 KV Cache？

回答：推理逐 token 生成，如果不缓存历史 token 的 K/V，每一步都要重复计算完整前缀，复杂度和延迟都会显著增加。

### Q3：Tokenizer 对 RAG 有什么影响？

回答：它影响 chunk 的 token 长度、上下文预算和召回内容能否完整放入 prompt；chunk size 应按 token 而不是字符估算。

## 内容选题

- 小红书：Token 不等于词，学大模型必须先搞懂 Tokenizer
- 视频：BPE 是怎么把一句话切成 token 的？
- 面试：训练时并行，推理时串行，为什么？
