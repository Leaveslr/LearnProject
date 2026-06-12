# 短视频脚本：Token 不等于词

## 选题

本期讲：Tokenizer 为什么是大模型输入入口。

## 开头 0-5 秒

```text
很多人以为 token 就是词，其实 token 可能是子词、字符、空格，甚至是特殊标记。
```

## 第一段 5-25 秒

```text
模型不能直接读字符串，要先走一遍：文本变 token，token 变 id，id 再进入 embedding。
Tokenizer 就决定了模型看到的基本单位。
```

画面：文本 -> token -> id -> embedding。

## 第二段 25-70 秒

```text
BPE 的直觉是从字符开始，不断合并高频相邻片段。
常见词切大块，生僻词拆小块。
所以它能在词表大小和序列长度之间折中。
```

画面：low / lower / newest 的合并示意。

## 第三段 70-100 秒

```text
Tokenizer 会影响推理成本、上下文长度、RAG chunk 和多语言效果。
所以做 RAG 时，chunk size 应该按 token 算，而不是只按字符算。
```

## 结尾

```text
一句话记住：token 不是词，而是模型词表里的基本单位。
```

