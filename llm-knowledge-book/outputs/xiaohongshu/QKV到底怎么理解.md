# 小红书图文笔记：Q/K/V 到底怎么理解？

## 标题候选

- Q/K/V 到底怎么理解？
- 一句话讲清楚 Attention
- 别再只背 Attention 公式了
- Attention 为什么要除以根号 d？
- Masked Attention 到底 mask 了什么？

## 推荐标题

Q/K/V 到底怎么理解？

## 封面文案

QKV 不是玄学

## 正文

很多人学 Attention，一上来就背公式：

```text
softmax(QK^T/sqrt(d))V
```

但面试更想听你讲清楚 Q/K/V 的角色。

一句话结论：

> Attention 是“先匹配，再取内容”。

### 1. Q/K/V 分别是什么？

- Q：当前 token 想找什么
- K：其他 token 怎么被匹配
- V：其他 token 提供什么内容

Q 和 K 算相关性，相关性再加权 V。

### 2. 用例子理解

句子里出现 `it` 时，模型要知道它指代谁。

`it` 的 Q 会去匹配前文 token 的 K，如果 `animal` 更相关，就从它的 V 拿更多信息。

### 3. 为什么要缩放？

维度大时，QK 点积会变大，softmax 容易饱和。

除以 `sqrt(d_k)` 是为了让数值更稳定。

### 4. Mask 是干嘛的？

自回归模型不能偷看未来。

所以 Decoder 的 Masked Self-Attention 只能看当前和历史 token。

## 面试回答卡

```text
Attention 通过 Q 和 K 计算相关性，
再用 softmax 得到权重，
最后对 V 加权求和得到上下文表示。
Q 表示当前 token 想找什么，
K 表示其他 token 如何被匹配，
V 表示真正提供的内容。
```

## 配图建议

- 图 1：Q 问 K，取 V。
- 图 2：Attention 四步流程。
- 图 3：causal mask 下三角矩阵。
- 图 4：误区卡。

## 标签

#大模型 #LLM #Attention #Transformer #AI面试

## 下一篇选题

Masked Self-Attention 为什么不能看未来？

