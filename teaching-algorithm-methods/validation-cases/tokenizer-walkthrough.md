# 流程走样例：Tokenizer

## 目标

把 Tokenizer 讲成“模型输入入口”，而不是只讲分词算法名。

## 1. 问题场景

神经网络不能直接读字符串。输入必须经过：

```text
文本 -> token -> token id -> embedding -> 模型
```

问题不是“怎么切词”这么简单，而是切出来的单位会影响序列长度、成本、多语言、代码和 RAG chunk。

## 2. 直觉模型

Tokenizer 像切拼图：常见片段切成大块，生僻片段拆成小块。

边界：token 不等于词。它可能是子词、字符、空格、标点、特殊角色标记。

## 3. 最小例子

```text
low / lower / newest
字符初始：l o w / l o w e r / n e w e s t
合并高频片段：low / er / est
```

BPE 的关键动作是合并高频相邻片段，不是理解语义。

## 4. 机制拆解

1. 文本清洗和规范化。
2. 子词切分。
3. token 映射成 token id。
4. 特殊 token 编码结构，如 BOS/EOS/system/user/tool。
5. token id 进入 embedding。

## 5. 工程取舍

- token 数越多，推理越贵。
- 词表越大，序列可能更短，但 embedding/output layer 更大。
- 中文、代码、特殊符号被切碎会浪费上下文。
- RAG chunk 应按 token 预算，而不是只按字符数。

## 6. 易错点和反例

- 错误：token 就是单词。反例：`unbelievable` 可能被切成多个子词。
- 错误：词表越大越好。反例：词表大也会增加参数和训练难度。
- 错误：Tokenizer 不影响应用。反例：chunk 超 token 预算会被截断。

## 7. 迁移练习

- 为什么代码模型要重视缩进和符号？
- 为什么同样 1000 字，中英文 token 数可能不同？
- Chat template 为什么也是 tokenizer 相关问题？

