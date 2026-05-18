# 第一章：Transformer 架构详解

## 1.1 Transformer 整体架构

Transformer 是一种基于注意力机制的神经网络架构，由 Google 在 2017 年提出（论文《Attention Is All You Need》）。它完全摒弃了传统的 RNN、CNN 结构，仅使用注意力机制来实现序列到序列的转换。

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

### 1.7.2 现代 FFN 变体

**SwiGLU（2026 年主流）**：
```python
class SwiGLU(nn.Module):
    def forward(self, x):
        return F.silu(x @ self.w1) * (x @ self.w3)
```
其中 W₂ 保持为 Gate。

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

## 面试高频追问

### Q1: Transformer 为何用 LayerNorm 而不是 BatchNorm？

> NLP 任务输入序列长度可变，LayerNorm 对单个样本归一化，更自然；BatchNorm 需要固定 batch 维度。

### Q2: Encoder 和 Decoder 如何交互？

> 通过 Cross-Attention：Decoder 的 Q 来自 Decoder，K、V 来自 Encoder 输出。

### Q3: 为什么要用带掩码 (Masked)？

> 解码器自回归生成时，不能看到未来 token，用 Masked 防止信息泄露。

---

*参考文献*
- Vaswani et al., "Attention Is All You Need", 2017
- FAQ_Of_LLM_Interview
