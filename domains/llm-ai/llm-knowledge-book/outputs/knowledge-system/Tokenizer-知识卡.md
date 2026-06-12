# 知识卡：Tokenizer

## 资料来源

- 主笔记：[Tokenizer 与语言模型基础](../../src/02-模型架构/00-Tokenizer与语言模型基础.md)

## 一句话结论

Tokenizer 决定模型看到的基本单位；它不是简单“分词器”，而是把文本、代码、角色标记和特殊符号变成 token id 的入口层。

## 它解决什么问题

- 神经网络不能直接处理字符串，必须先变成 token id。
- 纯 word-level 词表太大且有 OOV，纯 character-level 序列太长。
- Subword tokenizer 在词表大小、序列长度、多语言和生僻词之间折中。

## 核心直觉

- 一句话直觉：Tokenizer 像给语言切拼图，常见片段切大块，生僻片段切小块。
- 类比边界：token 不一定是词，可能是子词、空格、符号、中文字符、特殊标记。

## 最小例子

```text
lower / lowest / newest
先拆成字符，再不断合并高频相邻片段：
l o w -> low
e r -> er
e s t -> est
```

BPE 的结果不是“理解语义”，而是用统计频率得到可复用片段。

## 关键机制

1. 文本标准化：处理 unicode、空格、大小写等。
2. 子词切分：BPE/WordPiece/SentencePiece 生成 token。
3. 映射 id：token 进入 embedding 层。
4. 特殊 token：BOS/EOS/PAD/chat role/tool/image 等把结构塞进序列。

## 工程应用

- 影响上下文长度、推理成本、RAG chunk、代码模型效果和多语言表现。
- 中文或代码被切得更碎，会浪费上下文预算。
- Chat template 本质是把对话结构序列化成 token。

## 常见误区

- token 等于中文词或英文单词。
- 词表越大越好。
- tokenizer 只影响训练，不影响推理成本。

## 边界和反例

- OOV 不是完全消失，而是被拆成更小的已知片段。
- 词表过大虽然减少序列长度，但 embedding 和输出层参数会变大。
- 字符数相同的文本，token 数可能差很多。

## 面试追问

- BPE 为什么能缓解 OOV？
- Tokenizer 为什么会影响 RAG chunk？
- 为什么训练可并行，推理通常逐 token？

## 内容转化角度

- 小红书：Token 不等于词。
- 短视频：BPE 怎么切一句话。
- 面试卡：Tokenizer、chat template、next token prediction 一起答。

## 迁移练习

- 同型：解释代码 tokenizer 为什么要处理缩进和符号。
- 变式：比较中文和英文 token 数差异对成本的影响。
- 判断：词表越大一定越好吗？

