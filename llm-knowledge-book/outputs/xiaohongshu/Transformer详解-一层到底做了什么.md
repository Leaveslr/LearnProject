# 小红书图文笔记：Transformer 一层到底做了什么？

## 标题候选

- 大模型面试必问：Transformer 一层到底做了什么？
- 别再把 Transformer 理解成 Attention 了
- 一句话讲清楚 Transformer Block
- Transformer 的本质：沟通、加工、稳定
- 面试官问 Transformer，其实想听这 4 点
- Attention 只是 Transformer 的一半
- Transformer 为什么能替代 RNN？
- 大模型结构入门：Decoder-only 到底怎么工作？

## 推荐标题

别再把 Transformer 理解成 Attention 了

## 封面文案

Transformer 不只是 Attention

## 正文

很多人学 Transformer，一上来就背公式：

```text
Attention(Q,K,V)=softmax(QK^T/sqrt(d))V
```

但面试里只会背这个，基本不够。

因为 Transformer 不是一个 Attention 公式，而是一套让 token 反复“沟通、加工、稳定”的架构。

### 1. 先给结论

一句话理解 Transformer：

> Attention 负责从上下文拿信息，FFN 负责加工当前 token，Residual + Norm 负责让很多层稳定训练。

现代大模型通常堆很多层 Decoder-only Transformer Block，每一层都在做类似的事：

```text
token 表示
-> 和历史上下文沟通
-> 自己再加工一遍
-> 传给下一层
```

层数越多，token 表示就越“懂上下文”。

### 2. 用一个例子理解

假设输入是：

```text
我 今天 想 吃
```

模型要预测下一个 token，可能是“饭”“面”“苹果”。

这时最后一个 token“吃”不能只看自己，它需要参考：

- “我”：谁在说话
- “今天”：时间语境
- “想”：表达意愿
- “吃”：当前动作

Attention 做的就是：让“吃”这个位置去看前面哪些 token 更重要。

### 3. Transformer Block 里有 4 个关键部件

#### Attention：负责沟通

每个 token 都会生成 Q/K/V：

- Q：我想找什么信息
- K：我能被怎么匹配
- V：我真正提供什么内容

Q 和 K 算相关性，再用相关性加权 V。

直觉上就是：

```text
当前 token 问：谁对我有用？
其他 token 回：我这里有这些信息。
```

#### FFN：负责加工

Attention 拿到上下文后，FFN 会对每个 token 自己的表示做非线性加工。

它通常是：

```text
d_model -> d_ff -> d_model
```

也就是先扩维，再降维。

扩维是为了给模型更大的中间空间组合特征；降维是为了回到统一维度，继续传给下一层。

#### Residual：负责保留通路

残差连接大概长这样：

```text
x = x + attention(...)
x = x + ffn(...)
```

它的作用是保留原始信息，也让梯度更容易穿过很多层。

没有残差，深层 Transformer 会更难训练。

#### Norm：负责稳定尺度

Norm 用来稳定每层输入输出的数值尺度。

原始 Transformer 常讲 LayerNorm；现代 LLM 常见的是 Pre-Norm + RMSNorm。

可以这么记：

```text
Attention / FFN 负责表达
Residual 负责通路
Norm 负责稳定
```

### 4. 为什么现代大模型多是 Decoder-only？

原始 Transformer 是 Encoder-Decoder，适合机器翻译：

```text
源语言 -> Encoder -> Decoder -> 目标语言
```

但 GPT、LLaMA、Qwen 这类大语言模型的核心任务是：

```text
看历史 token，预测下一个 token
```

所以它们通常用 Decoder-only：

```text
历史 token -> 多层 Decoder Block -> 下一个 token 概率
```

Decoder-only 会加 causal mask，保证当前位置只能看历史，不能偷看未来。

### 5. 最容易混的误区

误区 1：Transformer = Attention  
正确理解：Attention 是核心，但 Transformer Block 还需要 FFN、Residual、Norm、位置编码。

误区 2：训练和推理都完全并行  
正确理解：训练时完整答案已知，可以用 mask 并行算 loss；推理时未来 token 还没生成，所以要逐 token 生成。

误区 3：Decoder-only 就是原始 Decoder  
正确理解：现代 LLM 通常没有 Cross-Attention，主要是 Masked Self-Attention + FFN。

## 面试回答卡

如果面试官问：Transformer 一层做了什么？

可以这样答：

```text
Transformer Block 主要包含 Attention、FFN、Residual 和 Norm。

Attention 负责让每个 token 从上下文中聚合相关信息；
FFN 对每个 token 的表示做非线性加工；
Residual 保留原始信息并改善梯度传播；
Norm 稳定每层的数值尺度。

现代大语言模型通常采用 Decoder-only 结构，
通过 causal mask 保证只能看历史 token，
再堆叠很多层 Transformer Block 来预测下一个 token。
```

## 配图建议

### 图 1：封面卡

```text
Transformer 不只是 Attention
它是一套沟通、加工、稳定的结构
```

### 图 2：Transformer Block 流程图

```text
Token 表示
  ↓
Norm -> Masked Self-Attention -> Residual
  ↓
Norm -> FFN / SwiGLU -> Residual
  ↓
下一层
```

### 图 3：四个部件对比表

| 部件 | 作用 | 一句话记忆 |
| --- | --- | --- |
| Attention | 上下文交互 | 和别人沟通 |
| FFN | 非线性加工 | 自己消化信息 |
| Residual | 信息/梯度通路 | 保留原始输入 |
| Norm | 稳定训练 | 控制数值尺度 |

### 图 4：常见误区卡

```text
别再说 Transformer = Attention
Attention 只是沟通
FFN 才负责加工
Residual + Norm 保证能堆深
```

### 图 5：面试回答卡

放“面试回答卡”中的 4 句话，适合收藏复习。

## 标签

#大模型 #LLM #Transformer #AI面试 #算法岗 #深度学习 #机器学习 #大模型面试

## 下一篇选题

下一篇可以继续拆：

- Q/K/V 到底为什么要拆成三套矩阵？
- Transformer 为什么不用 BatchNorm？
- Decoder-only 为什么适合大语言模型？
- KV Cache 到底缓存了什么？

