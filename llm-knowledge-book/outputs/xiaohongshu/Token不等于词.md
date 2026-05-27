# 小红书图文笔记：Token 不等于词

## 标题候选

- Token 不等于词，学大模型先搞懂这个
- 别再把 token 理解成单词了
- Tokenizer 到底在切什么？
- BPE 为什么能处理生僻词？
- 大模型成本，先从 token 数开始算

## 推荐标题

Token 不等于词，学大模型先搞懂这个

## 封面文案

Token 不是词

## 正文

很多人学大模型时，会把 token 理解成“一个中文词”或“一个英文单词”。

这个理解很容易误导。

一句话结论：

> Token 是模型词表里的基本单位，可能是子词、字符、空格、符号或特殊标记。

### 1. 为什么需要 Tokenizer？

模型不能直接读字符串，要先变成：

```text
文本 -> token -> token id -> embedding
```

Tokenizer 就是这个入口。

### 2. BPE 的直觉

BPE 会从字符开始，不断合并高频相邻片段。

常见词会被切得更大，生僻词会被拆成更小片段。

所以它既能控制词表，又能缓解 OOV。

### 3. 为什么它影响成本？

同一段话，不同 tokenizer 切出的 token 数可能不同。

token 越多：

- 上下文占用越多
- 推理成本越高
- RAG chunk 越容易被截断

### 4. 常见误区

误区：词表越大越好。  
正确：词表大可能减少序列长度，但 embedding 和输出层也会更大。

误区：chat template 只是 prompt 格式。  
正确：它最终也会变成 system/user/assistant 等特殊 token 序列。

## 面试回答卡

```text
Tokenizer 负责把文本转换成 token id。
现代 LLM 常用 subword tokenizer，
在词表大小和序列长度之间折中。
token 不等于词，它可能是子词、字符、符号或特殊标记。
Tokenizer 会影响上下文长度、推理成本、RAG chunk 和多语言表现。
```

## 配图建议

- 图 1：文本到 token id 流程。
- 图 2：word/char/subword 对比。
- 图 3：BPE 合并示意。
- 图 4：常见误区卡。

## 标签

#大模型 #LLM #Tokenizer #AI面试 #机器学习

## 下一篇选题

BPE 是怎么把一句话切成 token 的？

