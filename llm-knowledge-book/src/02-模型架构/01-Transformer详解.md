# 第一章：Transformer 架构详解

## 1.0 先建立直觉：Transformer 到底解决什么问题？

### 一句话结论

Transformer 是一种让序列中每个 token 都能直接“查看并整合”其他相关 token 信息的架构。现代大语言模型本质上是在堆叠很多个 Transformer Block，让每个 token 的表示不断吸收上下文，最后预测下一个 token。

### 它解决什么问题

在 Transformer 之前，处理文本序列常用 RNN/LSTM。RNN 的核心问题是：

- **顺序依赖强**：第 `t` 个位置必须等第 `t-1` 个位置算完，训练不容易并行。
- **长距离信息难传递**：很早出现的信息要经过很多步才能影响后面的 token。
- **表达瓶颈明显**：一个隐藏状态要压住前面所有信息，序列越长越吃力。

Transformer 的核心改进是：

- 用 **Self-Attention** 让任意两个 token 可以直接建立关系。
- 用 **多头注意力** 从不同角度看上下文关系。
- 用 **FFN、残差连接、LayerNorm** 稳定地堆很多层。
- 训练时可以对整段序列并行计算，特别适合 GPU。

### 初学者直觉

可以把 Transformer 想成一个“多人会议系统”：

- 每个 token 都像会议里的一个人。
- Self-Attention 让每个人根据当前问题，决定应该听谁多一点。
- Multi-Head Attention 像分多个讨论小组：有的头看语法关系，有的头看指代关系，有的头看主题关系。
- FFN 像每个人听完别人意见后，在自己脑子里做一次消化和加工。
- 多层 Transformer Block 就是多轮会议：第一轮看局部关系，后面逐渐形成更抽象的语义表示。

### 用一句话抓住主线

> Attention 负责“从上下文拿信息”，FFN 负责“加工当前 token 的信息”，残差和归一化负责“让很多层稳定训练”。

## 1.1 Transformer 整体架构

Transformer 是一种基于注意力机制的神经网络架构，由 Google 在 2017 年提出（论文《Attention Is All You Need》）。它不再依赖 RNN 的逐步递归，也不依赖 CNN 的局部卷积窗口，而是以注意力机制为核心，配合前馈网络、残差连接和归一化来处理序列。

### 1.1.1 经典架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      Transformer 架构                         │
├─────────────────────────────────────────────────────────────┤
│  Encoder (编码器)                        Decoder (解码器)    │
│  ┌─────────────────┐                   ┌─────────────────┐  │
│  │  Input Embedding │                   │  Output Embedding│  │
│  │       +         │                   │       +         │  │
│  │ Positional Enc. │                   │ Positional Enc. │  │
│  └────────┬────────┘                   └────────┬────────┘  │
│           │                                    │            │
│  ┌────────▼────────┐                   ┌────────▼────────┐  │
│  │  Encoder Layer 1 │◄────────┐       │  Decoder Layer 1 │  │
│  │  • Multi-Head    │         │       │  • Masked MHA    │  │
│  │    Self-Attention│         │       │  • Cross-Attention│  │
│  │  • Feed Forward  │         │       │  • Feed Forward   │  │
│  └────────┬────────┘         │       └────────┬────────┘  │
│           │                  │                │            │
│  │        ▼                  │                ▼            │
│  │  Encoder Layer 2 │       │       │  Decoder Layer 2 │  │
│  │       ...          │       │       │       ...         │  │
│  └────────┬────────┘         │       └────────┬────────┘  │
│           │                  │                │            │
│           ▼                  │                │            │
│  ┌─────────────────┐        │       ┌────────▼────────┐  │
│  │  N × Encoder    │─────────┼──────►│  Cross-Attention │  │
│  │     Layers      │         │       │  (使用Encoder输出)│  │
│  └────────┬────────┘         │       └────────┬────────┘  │
│           │                  │                │            │
│           ▼                  │                ▼            │
│  ┌─────────────────┐        │       ┌─────────────────┐  │
│  │   Encoder       │        │       │   Linear +      │  │
│  │   Output        │────────┘       │   Softmax       │  │
│  └─────────────────┘                └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 1.1.2 核心组件

| 组件 | 位置 | 作用 |
|------|------|------|
| **Input Embedding** | Encoder | 将输入 token 转换为向量表示 |
| **Positional Encoding** | 两者 | 注入位置信息（Transformer 本身无位置感知） |
| **Multi-Head Self-Attention** | Encoder | 编码器内部：所有位置互相 attend |
| **Masked Multi-Head Self-Attention** | Decoder | 解码器内部：只能 attend 到之前的位置 |
| **Cross-Attention** | Decoder | 解码器关注编码器的输出 |
| **Feed Forward Network** | 两者 | 非线性变换，提升模型表达能力 |
| **Layer Normalization** | 两者 | 稳定训练、加速收敛 |
| **Residual Connection** | 两者 | 缓解梯度消失/爆炸 |

### 1.1.3 原始 Transformer 与现代 LLM 的关系

原始 Transformer 是 **Encoder-Decoder** 架构，主要用于机器翻译：

```text
源语言句子 -> Encoder 理解整句 -> Decoder 逐词生成目标语言
```

现代 GPT、LLaMA、Qwen 等大语言模型通常采用 **Decoder-only Transformer**：

```text
历史 token -> 多层 Decoder Block -> 预测下一个 token
```

二者的关键区别：

| 架构 | 典型模型 | 注意力方式 | 主要用途 |
| --- | --- | --- | --- |
| Encoder-only | BERT | 双向 Self-Attention | 理解、分类、检索、抽取 |
| Encoder-Decoder | T5、原始 Transformer | Encoder 双向 + Decoder 因果 + Cross-Attention | 翻译、摘要、条件生成 |
| Decoder-only | GPT、LLaMA、Qwen、DeepSeek | 因果 Masked Self-Attention | 自回归生成、对话、代码生成 |

讲大模型结构时，重点应放在 Decoder-only：它没有 Encoder，也通常没有 Cross-Attention；每一层主要由 **Masked Self-Attention + FFN + 残差/归一化** 组成。

---

## 1.2 Encoder 详解

### 1.2.1 Encoder Layer 结构

```
Input
  │
  ▼
┌──────────────────────────────┐
│   Multi-Head Self-Attention   │
│                              │
│   Q = XW_Q, K = XW_K, V = XW_V
│   Attention(Q,K,V) = softmax(QK^T/√d)V
│                              │
└──────────────┬───────────────┘
               │ (Residual + LayerNorm)
               ▼
┌──────────────────────────────┐
│      Feed Forward Network    │
│                              │
│   FFN(x) = max(0, xW₁+b₁)W₂+b₂
│   (或 SwiGLU 变体)           │
└──────────────┬───────────────┘
               │ (Residual + LayerNorm)
               ▼
             Output
```

### 1.2.2 编码器核心特点

1. **双向注意力**：每个位置可以 attend 到序列中的所有其他位置
2. **无掩码**：信息流通无限制
3. **堆叠 N 层**：原始论文使用 N=6

---

## 1.3 Decoder 详解

### 1.3.1 Decoder Layer 结构

```
Output(t-1)                        Encoder Output
    │                                   │
    ▼                                   │
┌─────────────────────┐                 │
│ Masked Multi-Head   │                 │
│ Self-Attention      │                 │
│ (只能看到之前的token) │                 │
└──────────┬──────────┘                 │
           │                             │
           │ (Residual + LayerNorm)     │
           ▼                             │
┌─────────────────────┐                 │
│  Cross-Attention     │◄────────────────┤
│  Q来自Decoder        │                 │
│  K,V来自Encoder      │                 │
└──────────┬──────────┘                 │
           │                             │
           │ (Residual + LayerNorm)     │
           ▼                             │
┌─────────────────────┐                 │
│      FFN            │                 │
└──────────┬──────────┘                 │
           │                             │
           ▼                             │
        Output(t)
```

### 1.3.2 解码器核心特点

1. **因果掩码 (Causal Mask)**：防止看到未来位置
2. **Cross-Attention**：从编码器输出中提取信息
3. **自回归生成**：逐 token 生成

### 1.3.3 现代 LLM 的 Decoder-only Block

现代大模型常见的单层结构可以理解为：

```text
x
│
├─ Norm -> Masked Self-Attention -> Residual Add
│
└─ Norm -> FFN / SwiGLU -> Residual Add
```

也就是：

```python
x = x + attention(norm(x), causal_mask=True)
x = x + ffn(norm(x))
```

注意：不同模型可能采用 **Pre-LN**、**RMSNorm**、**RoPE**、**GQA/MLA**、**SwiGLU** 等变体，但主线仍然是“注意力拿上下文信息，FFN 做非线性加工”。

---

## 1.4 为什么使用多头注意力？

### 1.4.1 多头注意力的优势

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads
        
        # 多个注意力头可以关注不同的语义子空间
        self.W_Q = nn.Linear(d_model, d_model)
        self.W_K = nn.Linear(d_model, d_model)
        self.W_V = nn.Linear(d_model, d_model)
        self.W_O = nn.Linear(d_model, d_model)
    
    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)
        
        # 分割成多个头
        Q = self.W_Q(Q).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.W_K(K).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.W_V(V).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)
        
        # 注意力计算
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        attention_weights = F.softmax(scores, dim=-1)
        output = torch.matmul(attention_weights, V)
        
        # 合并多头
        output = output.transpose(1, 2).contiguous().view(batch_size, -1, self.num_heads * self.head_dim)
        return self.W_O(output)
```

### 1.4.2 多头注意力的三个优势

| 优势 | 说明 |
|------|------|
| **多子空间学习** | 不同头可以学习关注不同的语义关系（语法、实体、语义等） |
| **提高模型容量** | 矩阵整体 size 不变，只是改变每个 head 对应的维度大小 |
| **硬件并行** | 充分利用 GPU 并行计算能力 |

---

## 1.5 Q/K/V 为何使用不同权重矩阵？

### 1.5.1 设计动机

Transformer 中使用不同的权重矩阵生成 Q、K、V，是为了对输入 X 进行**线性变换**，提升模型拟合能力。

```python
# 核心计算
Q = X @ W_Q  # Query: 我要找什么
K = X @ W_K  # Key: 我有什么
V = X @ W_V  # Value: 我的内容是什么
```

### 1.5.2 为什么不能共享权重？

1. **表达能力**：Q、K、V 需要捕捉不同的语义特征
   - Q 需要"查询"能力
   - K 需要"匹配"能力
   - V 需要"内容表达"能力

2. **数学独立性**：如果共享权重，模型会退化为简化版本

---

## 1.6 残差连接与层归一化

### 1.6.1 残差连接 (Residual Connection)

**目的**：解决神经网络的"退化现象"

```python
# 残差连接的核心思想
output = x + SubLayer(x)  # 跳跃连接
```

**优势**：
- 缓解梯度消失/爆炸
- 使得深层网络更易训练
- 信息直接传递

### 1.6.2 层归一化 (Layer Normalization)

**公式**：
```
LN(x) = γ * (x - μ) / σ + β
```

其中：
- μ = mean(x)
- σ = std(x)
- γ, β 为可学习参数

**为什么 Transformer 用 LN 而不是 BN？**

| 特性 | LayerNorm | BatchNorm |
|------|-----------|-----------|
| 归一化维度 | 单个样本的所有特征 | Batch 维度 |
| 序列数据支持 | ✅ 自然处理可变长度 | ❌ 需固定 batch size |
| NLP 适用性 | ✅ 适合变长序列 | ❌ 不适合 |

### 1.6.3 归一化选择：BatchNorm、LayerNorm、RMSNorm

Stanford CS224N 的 Transformer notes 提醒我们，理解 LayerNorm 时最关键的问题是：**统计量到底是沿哪个维度算的？** 在 Transformer 里，LayerNorm 通常对“单个样本、单个 token 位置”的 hidden 维度计算均值和方差；也就是说，第 `i` 个 token 的统计量不会影响第 `j` 个 token，也不会依赖 batch 里其他样本。

如果输入张量是：

```text
x: [batch_size, seq_len, hidden_dim]
```

那么不同归一化可以粗略理解为：

| 方法 | 统计量主要沿哪个维度算 | 是否依赖 batch | Transformer 中的常见性 | 直觉 |
| --- | --- | --- | --- | --- |
| BatchNorm | batch 维度，常用于同一 feature/channel | 依赖 | 少见 | 用一批样本的统计量稳定激活 |
| LayerNorm | 单个 token 的 hidden_dim | 不依赖 | 标准选择 | 每个 token 自己把特征尺度拉稳 |
| RMSNorm | 单个 token 的 hidden_dim，但只用均方根，不减均值 | 不依赖 | 现代 LLM 常见 | 更轻量的 LayerNorm 变体 |

#### 为什么 Transformer 很少用 BatchNorm？

1. **序列长度可变**：NLP batch 常有 padding，不同样本长度不一，按 batch 统计会引入额外复杂性。
2. **自回归推理 batch 不稳定**：推理时可能 batch size 很小甚至为 1，BatchNorm 的训练/推理统计不一致会更麻烦。
3. **分布式训练通信成本**：大模型训练常做 tensor/pipeline/data parallel，如果依赖跨 batch 统计，同步会增加通信。
4. **token 表示应独立稳定**：Transformer 更希望每个 token 的表示在自己的 hidden 维度内被稳定，而不是被同 batch 其他句子影响。

#### Pre-LN vs Post-LN

原始 Transformer 图里常见的是 Post-LN：

```text
x -> Sublayer -> Add Residual -> LayerNorm
```

写成公式：

```text
y = LN(x + Sublayer(x))
```

现代大模型更常见的是 Pre-LN：

```text
x -> LayerNorm -> Sublayer -> Add Residual
```

写成公式：

```text
y = x + Sublayer(LN(x))
```

面试里可以这样回答：

- **Post-LN** 更贴近原始 Transformer，但深层模型训练时梯度更容易不稳定。
- **Pre-LN** 让残差主路径更像一条干净的梯度高速路，深层 Transformer 更容易训练。
- 现代 LLM 通常采用 Pre-LN 或其变体，再配合最后的 final norm。

#### LayerNorm vs RMSNorm

LayerNorm：

```text
LN(x) = gamma * (x - mean(x)) / sqrt(var(x) + eps) + beta
```

RMSNorm：

```text
RMSNorm(x) = gamma * x / sqrt(mean(x^2) + eps)
```

区别：

- LayerNorm 会减均值并除以标准差。
- RMSNorm 不减均值，只按均方根缩放。
- RMSNorm 计算更简单，现代 LLM 中常见，例如 LLaMA 系列使用 RMSNorm。

选择原则：

- 传统 Transformer/BERT/T5 体系：LayerNorm 是标准答案。
- GPT/LLaMA/Qwen 等现代 decoder-only LLM：常见 Pre-Norm + RMSNorm。
- CNN/视觉卷积网络：BatchNorm 仍然常见。
- 小 batch、变长序列、自回归生成：优先 LayerNorm/RMSNorm，而不是 BatchNorm。

---

## 1.7 Feed Forward Network

### 1.7.1 标准 FFN

```python
class FFN(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.w1 = nn.Linear(d_model, d_ff)
        self.w2 = nn.Linear(d_ff, d_model)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        return self.w2(self.relu(self.w1(x)))
```

### 1.7.2 为什么 FFN 要先扩维再降维？

Transformer Block 里的 Attention 负责跨 token 沟通，但每个 token 拿到上下文信息后，还需要一个非线性网络做“消化”。FFN 通常会把维度从 `d_model` 扩到更大的 `d_ff`，再降回 `d_model`：

```text
d_model -> d_ff -> d_model
```

直觉：

- 扩维：给模型更大的中间空间去组合特征。
- 激活函数：引入非线性，否则多层线性变换可以合并成一层。
- 降维：回到统一的 `d_model`，方便和残差连接、下一层 Transformer Block 对接。

面试短答：

> Attention 决定“从上下文拿什么”，FFN 决定“拿到后怎么加工”。扩维再降维是为了提供更强的非线性表达能力，同时保持每层输入输出维度一致。

### 1.7.3 现代 FFN 变体

**SwiGLU（现代 LLM 常用）**：
```python
class SwiGLU(nn.Module):
    def forward(self, x):
        hidden = F.silu(x @ self.w_gate) * (x @ self.w_up)
        return hidden @ self.w_down
```

直觉上，SwiGLU 相当于给 FFN 加了一个“门控”：一部分通道负责产生候选信息，另一部分通道决定哪些信息应该通过。

---

## 1.8 CNN vs Transformer

| 特性 | CNN | Transformer |
|------|-----|-------------|
| **核心操作** | 卷积 | 自注意力 |
| **感受野** | 局部 → 全局（多层堆叠） | 全局（单层即可） |
| **并行化** | 受限于卷积核滑动 | 完全并行 |
| **位置建模** | 天然隐含位置 | 需额外注入位置编码 |
| **计算复杂度** | O(n·k·d) | O(n²·d) |
| **适用场景** | 图像、音频 | 文本、多模态 |

---

## 1.9 梯度消失与爆炸

### 1.9.1 问题原因

梯度消失与梯度爆炸其实是一种情况的两个极端：

1. **深层网络**：不同层学习速度差异大
2. **激活函数**：如 sigmoid 导数最大 0.25

### 1.9.2 解决方案

| 方案 | 原理 |
|------|------|
| **残差连接** | 梯度直接回传，缓解消失 |
| **层归一化** | 稳定梯度分布 |
| **合适激活函数** | ReLU、SwiGLU 等 |
| **梯度裁剪** | 限制梯度范围 |
| **Xavier/He 初始化** | 合理初始化权重 |

---

## 1.10 用一个例子走完整流程：大模型如何预测下一个词？

### 问题场景

假设输入是：

```text
我 今天 想 吃
```

大模型要预测下一个 token，可能是：

```text
饭 / 面 / 苹果 / ...
```

Transformer 做的事情不是简单记忆“想吃后面常接什么”，而是让每个 token 在多层网络中不断吸收上下文，最终用最后一个位置的表示去预测下一个 token。

### 第一步：Token 变成向量

```text
我 -> embedding_1
今天 -> embedding_2
想 -> embedding_3
吃 -> embedding_4
```

这些向量最开始只是 token 的基础表示，还不知道当前句子的上下文关系。

### 第二步：加入位置信息

Self-Attention 本身不天然知道顺序。如果只看一组 token 向量，模型不知道“我 今天 想 吃”和“吃 想 今天 我”的区别。

所以要加入位置编码，现代 LLM 常用 RoPE 等方式把位置信息注入 Q/K。

### 第三步：Masked Self-Attention 拿上下文

当模型处理“吃”这个位置时，它可以看见：

```text
我、今天、想、吃
```

但不能看见未来 token。因果 mask 保证训练时不会偷看答案。

注意力大致会做：

```text
当前 token 的 Query：我现在要找什么信息？
历史 token 的 Key：我能提供什么线索？
历史 token 的 Value：我实际贡献什么内容？
```

然后根据相关性对历史信息加权求和，得到“吃”这个位置的新表示。

### 第四步：FFN 加工每个位置的信息

Attention 更像“跨 token 沟通”，FFN 更像“每个 token 自己消化信息”。

```text
上下文表示 -> FFN -> 更强的语义特征
```

多层堆叠后，最后一个 token 的表示会逐渐包含：

- 句子主题：今天、吃东西。
- 语法关系：想吃后面通常接食物。
- 世界知识：饭、面、水果都可能，但“天气”不太合理。

### 第五步：Linear + Softmax 预测下一个 token

最后一层输出会经过线性层映射到词表大小：

```text
hidden_state_of_last_token -> logits over vocabulary -> softmax -> token probability
```

模型得到类似概率分布：

```text
饭: 0.31
面: 0.22
苹果: 0.08
天气: 0.001
```

推理时再通过 greedy decoding、top-k、top-p、temperature 等策略选择下一个 token。

### 关键检查问题

- 为什么 Decoder-only 模型要用 causal mask？
- 为什么 Self-Attention 需要额外的位置信息？
- Attention 和 FFN 分别在做什么？
- 为什么训练时可以并行，但生成时通常要逐 token 生成？

### 常见误区与反例

| 误区 | 正确理解 |
| --- | --- |
| Transformer 只有 Attention | Transformer Block 还包含 FFN、残差、归一化、位置编码等关键组件 |
| Decoder-only 等于原始 Transformer Decoder | 现代 LLM 通常去掉 Cross-Attention，只保留因果 Self-Attention 和 FFN |
| Attention 权重就是完整解释 | 注意力权重能提供线索，但不能直接等同于模型推理解释 |
| 训练和生成都是完全并行 | 训练时整段序列可并行；自回归生成时下一个 token 依赖前面已生成 token |

---

## 面试高频追问

### Q1: Transformer 为何用 LayerNorm 而不是 BatchNorm？

> NLP 任务输入序列长度可变，LayerNorm 对单个样本归一化，更自然；BatchNorm 需要固定 batch 维度。

### Q2: Encoder 和 Decoder 如何交互？

> 通过 Cross-Attention：Decoder 的 Q 来自 Decoder，K、V 来自 Encoder 输出。

### Q3: 为什么要用带掩码 (Masked)？

> 解码器自回归生成时，不能看到未来 token，用 Masked 防止信息泄露。

### Q4: 为什么现代大模型多用 Decoder-only 架构？

> 大语言模型的核心任务是根据历史上下文预测下一个 token。Decoder-only 的因果注意力天然匹配自回归生成目标，结构简单、训练和推理路径一致，易于规模化扩展。

### Q5: Attention 和 FFN 的分工是什么？

> Attention 负责 token 之间的信息交互，决定当前位置应该从上下文哪些位置拿信息；FFN 负责对每个位置的表示做非线性变换，提升特征表达能力。可以粗略理解为：Attention 做“沟通”，FFN 做“消化”。

### Q6: BatchNorm 和 LayerNorm 的核心区别是什么？

> BatchNorm 主要沿 batch 维度统计，同一个 feature/channel 会参考一批样本的均值和方差；LayerNorm 主要沿单个样本、单个 token 的 hidden 维度统计，不依赖 batch。Transformer 处理变长序列和自回归生成时，更适合使用 LayerNorm。

### Q7: 为什么 Transformer 中 LayerNorm 通常比 BatchNorm 更合适？

> 因为 NLP 序列长度可变、batch 内 padding 多、推理时 batch size 可能很小，并且大模型分布式训练不希望额外同步 batch 统计量。LayerNorm 对每个 token 独立归一化，训练和推理行为更一致。

### Q8: Pre-LN 和 Post-LN 有什么区别？

> Post-LN 是 `LN(x + Sublayer(x))`，更接近原始 Transformer；Pre-LN 是 `x + Sublayer(LN(x))`，现代大模型更常用。Pre-LN 保留了更直接的残差梯度路径，深层 Transformer 更容易训练。

### Q9: 为什么现代 LLM 常用 RMSNorm？

> RMSNorm 可以看作更轻量的 LayerNorm：它不减均值，只用均方根缩放 hidden 向量。它计算更简单，在大规模 decoder-only 模型中常见，通常和 Pre-Norm 结构一起使用。

### Q10: LayerNorm 是对整个句子做归一化吗？

> 不是。Transformer 里的 LayerNorm 通常是对每个 token 位置单独做归一化，只在该 token 的 hidden 维度上计算均值和方差。一个 token 的归一化统计量不会来自另一个 token。

### Q11: 归一化、残差连接、Attention、FFN 之间是什么关系？

> Attention 和 FFN 是主要变换；残差连接让原始信息和梯度能稳定穿过很多层；归一化控制每层输入/输出的尺度，减少训练不稳定。可以记成：Attention/FFN 负责表达，Residual 负责通路，Norm 负责尺度稳定。

### Q12: 面试中如何回答“Transformer 的归一化怎么选”？

> 如果问原始 Transformer，答 LayerNorm + Add&Norm；如果问现代 LLM，答 Pre-Norm 更常见，很多 decoder-only 模型使用 RMSNorm；如果问为什么不用 BatchNorm，强调变长序列、小 batch/自回归推理、分布式同步成本和 token 独立归一化。

---

*参考文献*
- Vaswani et al., "Attention Is All You Need", 2017
- Stanford CS224N, "Self-Attention & Transformers" notes
- Stanford CS224N lecture materials, "LayerNorm, standard in Transformers"
- MIT Vision Book, "Transformers"
- FAQ_Of_LLM_Interview
