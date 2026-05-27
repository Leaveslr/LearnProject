# 面试卡：Tokenizer

## 高频问法

- Tokenizer 是什么？token 和词有什么区别？
- BPE 为什么能缓解 OOV？
- Tokenizer 对 RAG 和成本有什么影响？

## 30 秒回答

Tokenizer 负责把文本转成模型能处理的 token id。现代 LLM 多用 subword tokenizer，在词表大小和序列长度之间折中。token 不一定等于词，可能是子词、字符、空格或特殊标记。Tokenizer 会影响上下文长度、推理成本、多语言、代码和 RAG chunk。

## 2 分钟回答

神经网络不能直接处理字符串，需要经过“文本 -> token -> token id -> embedding”。Word-level 直观但词表大且有 OOV，character-level 词表小但序列长，subword 是折中。BPE 从字符开始合并高频相邻片段，让常见词用更少 token，生僻词拆成已知子词。工程上，token 数影响计算成本和上下文预算，chat template 也依赖特殊 token 把 system/user/assistant/tool 等结构编码进序列。

## 追问

### Q1：BPE 为什么能缓解 OOV？

回答：因为它保留子词和字符级 fallback，没见过的词可以拆成已知片段。

### Q2：Tokenizer 对 RAG 有什么影响？

回答：chunk size、上下文预算和截断都应按 token 估算，不同 tokenizer 下同一段文本 token 数可能不同。

### Q3：词表越大越好吗？

回答：不一定。词表大可减少序列长度，但 embedding 和输出层参数也会增加，还可能影响训练和泛化。

## 容易翻车

- 错误：token 就是词。
- 正确：token 是模型词表里的单位，可能是子词、字符、符号或特殊标记。

