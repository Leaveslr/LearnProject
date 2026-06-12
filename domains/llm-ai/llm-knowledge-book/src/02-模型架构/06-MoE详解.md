# 第八章：混合专家模型 MoE

## 8.1 MoE 概述

### 8.1.1 什么是 MoE？

MoE（Mixture of Experts，混合专家）是一种**条件计算**技术，通过动态选择部分"专家"网络来处理不同输入，在保持模型总容量巨大的同时，降低实际计算成本。

```
┌─────────────────────────────────────────────────────────────┐
│                    MoE vs Dense 模型                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Dense 模型:                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  所有输入 → 所有参数 → 每次都激活全部计算              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  MoE 模型:                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  输入 → Router → 选择 Top-K 专家                     │   │
│  │         ↓                                           │   │
│  │  Expert 1  Expert 2  ...  Expert N                  │   │
│  │         ↓                                           │   │
│  │  加权融合 → 输出                                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  例如: 8个专家，选Top-2 → 只激活 2/8 = 25% 的专家           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 8.1.2 MoE 的核心优势

| 指标 | Dense | MoE |
|------|-------|-----|
| **参数量** | 固定 | 可扩展至巨大 |
| **激活参数** | 全部 | 仅选择的专家 |
| **计算量** | O(全部参数) | O(选中的专家) |
| **推理效率** | 固定 | 高（稀疏激活） |

---

## 8.2 MoE 架构详解

### 8.2.1 核心组件

```
┌─────────────────────────────────────────────────────────────┐
│                      MoE Layer 结构                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                    输入 X                                    │
│                       │                                     │
│                       ▼                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   Router / Gating                    │   │
│  │                                                      │   │
│  │   Router: W_routing · X → 专家得分                  │   │
│  │   Softmax: 归一化为专家选择概率                      │   │
│  │   Top-K:  选择得分最高的 K 个专家                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                       │                                     │
│     ┌─────────────────┼─────────────────┐                    │
│     ▼                 ▼                 ▼                    │
│  Expert 1          Expert 2        Expert N               │
│  (FFN)             (FFN)           (FFN)                    │
│     │                 │                 │                    │
│     └─────────────────┼─────────────────┘                    │
│                       ▼                                     │
│               加权求和: Σ weight_i × Expert_i(X)            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 8.2.2 组件详解

| 组件 | 功能 | 说明 |
|------|------|------|
| **Router/Gating** | 决定输入由哪些专家处理 | 通常是一个轻量级网络 |
| **Expert** | 实际的计算单元 | 通常是 FFN |
| **Top-K Selection** | 稀疏激活的关键 | 只激活 K 个专家 |
| **Load Balancer** | 平衡专家负载 | 防止负载不均 |

---

## 8.3 Router 机制

### 8.3.1 Router 计算过程

```python
class MoELayer(nn.Module):
    def __init__(self, d_model, num_experts, top_k):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k
        
        # Router 网络
        self.gate = nn.Linear(d_model, num_experts, bias=False)
        
        # 多个专家
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(d_model, d_ff),
                nn.ReLU(),
                nn.Linear(d_ff, d_model)
            )
            for _ in range(num_experts)
        ])
    
    def forward(self, x):
        # 1. 计算专家得分
        gate_logits = self.gate(x)  # [batch, seq, num_experts]
        
        # 2. Softmax 得到概率
        gate_probs = F.softmax(gate_logits, dim=-1)
        
        # 3. 选择 Top-K
        top_k_probs, top_k_indices = torch.topk(gate_probs, self.top_k, dim=-1)
        
        # 4. 归一化
        top_k_probs = top_k_probs / top_k_probs.sum(dim=-1, keepdim=True)
        
        # 5. 专家计算 + 加权求和
        output = torch.zeros_like(x)
        for i in range(self.top_k):
            expert_idx = top_k_indices[:, :, i]
            expert_weight = top_k_probs[:, :, i]
            
            # 收集对应专家的输出
            for e in range(self.num_experts):
                mask = (expert_idx == e)
                if mask.any():
                    e_output = self.experts[e](x[mask])
                    output[mask] += expert_weight[mask].unsqueeze(-1) * e_output
        
        return output
```

---

## 8.4 负载均衡

### 8.4.1 为什么需要负载均衡？

如果 Router 总是选择同一个专家：
1. 该专家过载，计算瓶颈
2. 其他专家得不到训练，能力退化

### 8.4.2 辅助损失函数

```python
def auxiliary_loss(gate_logits, expert_indices, num_experts):
    """
    负载均衡辅助损失
    """
    # 1. 计算每个专家被选中的频率
    # shape: [num_experts]
    expert_counts = F.one_hot(expert_indices, num_experts).sum(dim=[0, 1])
    expert_fraction = expert_counts / expert_indices.numel()
    
    # 2. 计算 Router 给每个专家的平均概率
    gate_probs = F.softmax(gate_logits, dim=-1)
    expert_probs = gate_probs.mean(dim=[0, 1])  # 按专家维度平均
    
    # 3. 辅助损失 = 频率 × 概率
    # 目标：让两者都接近均匀分布 (1/num_experts)
    return num_experts * (expert_fraction * expert_probs).sum()
```

### 8.4.3 无损负载均衡（Auxiliary-Loss-Free）

DeepSeek-V3 提出的方法：

```python
class AuxLossFreeMoE(nn.Module):
    def __init__(self):
        self.biases = nn.Parameter(torch.zeros(num_experts))
    
    def forward(self, x):
        # Router 计算
        scores = self.gate(x) + self.biases
        
        # Top-K 选择时使用调整后的分数
        top_k_scores, top_k_indices = torch.topk(scores, self.top_k, dim=-1)
        
        # 动态调整偏置（训练过程中）
        # 如果某专家负载过高，降低其偏置
```

---

## 8.5 MoE 的代表性模型

### 8.5.1 模型对比

| 模型 | 专家数 | Top-K | 总参数量 | 激活参数量 |
|------|--------|-------|---------|-----------|
| Mixtral 8x7B | 8 | 2 | 46.7B | 12.9B |
| DBRX | 16 | 4 | 132B | 36B |
| DeepSeek-V2 | 128 | 8 | 236B | 21B |
| Switch Transformer | 2048 | 1 | 1.6T | 8B |

### 8.5.2 Mixtral 8x7B 架构

```python
# Mixtral 8x7B 核心结构
class MixtralBlock(nn.Module):
    def __init__(self):
        self.attention = GQA(num_kv_heads=8, num_q_heads=32)
        self.moe = MoELayer(
            num_experts=8,
            top_k=2,  # 每次选择 2 个专家
            d_model=4096,
            d_ff=14336
        )
        self.norm = RMSNorm()
    
    def forward(self, x):
        x = x + self.attention(self.norm(x))
        x = x + self.moe(self.norm(x))
        return x
```

---

## 8.6 面试高频问题

### Q1: 什么是 MoE？为什么需要它？

> MoE（混合专家）是一种条件计算技术。对于每个输入，动态选择部分专家网络处理，而不是所有网络都参与计算。这样可以在巨大参数量下保持高效推理。

### Q2: MoE 的负载均衡怎么实现？

> 常见方法：1）辅助损失函数，惩罚不均衡的专家选择；2）无损负载均衡，通过动态调整专家偏置来平衡；3）专家容量限制。

### Q3: MoE 相比 Dense 模型的优势？

> 1）相同推理成本下可以有更多参数；2）稀疏激活，计算效率高；3）不同专家可学习不同领域的知识。

### Q4: MoE 的挑战有哪些？

> 1）负载均衡问题；2）通信开销（分布式训练）；3）显存占用（所有专家参数需加载）；4）调优复杂度高。

---

*参考文献*
- Shazeer et al., "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer", 2017
- Jiang et al., "Mixtral of Experts", 2024
- DeepSeek Team, "DeepSeek-V2", 2024
