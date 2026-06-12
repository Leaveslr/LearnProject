# 第九章：LoRA 原理与实战

## 9.1 LoRA 概述

### 9.1.1 什么是 LoRA？

LoRA（Low-Rank Adaptation）是一种**参数高效微调**（PEFT）技术，通过引入低秩矩阵来近似参数更新，以极少的可训练参数实现模型微调。

```
┌─────────────────────────────────────────────────────────────┐
│                    LoRA 核心思想                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  全参数微调:                                                │
│  W_new = W_0 + ΔW                                          │
│  ΔW 是完整矩阵 d×k，与 W_0 相同规模                        │
│                                                              │
│  LoRA:                                                      │
│  ΔW = B · A    (低秩分解)                                  │
│  W_new = W_0 + B·A                                         │
│                                                              │
│  其中: A ∈ R^(r×k), B ∈ R^(d×r), r << min(d,k)            │
│                                                              │
│  可训练参数: d×r + k×r ≈ O(r(d+k))                        │
│  相比完整参数: d×k                                          │
│                                                              │
│  例如: d=k=4096, r=8                                        │
│  完整参数: 16,777,216                                       │
│  LoRA参数: 65,536 (减少 99.6%)                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 9.1.2 LoRA 的优势

| 特性 | 全参数微调 | LoRA |
|------|-----------|------|
| **可训练参数** | 100% | < 1% |
| **显存需求** | 高 | 低 |
| **训练速度** | 慢 | 快 |
| **模型切换** | 需保存完整权重 | 只需保存适配器 |
| **性能** | 最优 | 可接近全参数微调 |

---

## 9.2 LoRA 原理详解

### 9.2.1 低秩假设

LoRA 基于一个关键假设：**预训练模型在下游任务中的微调过程中，权重更新具有低内在秩（low intrinsic rank）**。

```
ΔW 可以分解为两个低秩矩阵的乘积: ΔW = B · A

为什么低秩？
- 预训练已经学会了大量通用知识
- 微调只需要在低维子空间调整即可
- 高维更新可能是冗余的
```

### 9.2.2 数学公式

```python
# 前向传播
h = W_0 · x + (α/r) · B · A · x

# 其中:
# W_0: 预训练权重（冻结）
# A: 下采样矩阵 (r × k)，用高斯分布初始化
# B: 上采样矩阵 (d × r)，用零初始化
# α: 缩放因子（通常设为 r 的值）
# r: 秩（rank）
```

### 9.2.3 为什么 B 用零初始化？

```python
# 初始化策略
A = torch.randn(r, k) * std  # 高斯分布
B = torch.zeros(d, r)          # 零初始化

# 效果: 训练开始时 BA = 0，所以 W_new = W_0
# 相当于没有进行任何改变，然后逐渐学习
```

---

## 9.3 LoRA 代码实现

### 9.3.1 基本实现

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class LoRALinear(nn.Module):
    def __init__(self, in_features, out_features, rank=8, alpha=16):
        super().__init__()
        self.rank = rank
        self.alpha = alpha
        
        # 冻结原始权重
        self.weight = nn.Parameter(
            torch.randn(out_features, in_features), 
            requires_grad=False
        )
        
        # LoRA 可训练参数
        self.lora_A = nn.Parameter(torch.randn(rank, in_features) * 0.01)
        self.lora_B = nn.Parameter(torch.zeros(out_features, rank))
    
    def forward(self, x):
        # 原始输出
        base_output = F.linear(x, self.weight)
        
        # LoRA 输出
        lora_output = (self.lora_B @ self.lora_A) @ x.t()
        
        # 缩放并合并
        return base_output + (self.alpha / self.rank) * lora_output.t()
```

### 9.3.2 使用 PEFT 库

```python
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM

# 加载基础模型
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3-8B")

# LoRA 配置
lora_config = LoraConfig(
    r=16,                                    # 秩
    lora_alpha=32,                          # 缩放因子
    target_modules=[                         # 应用 LoRA 的层
        "q_proj", "v_proj", "k_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# 应用 LoRA
model = get_peft_model(model, lora_config)

# 查看可训练参数
model.print_trainable_parameters()
# 输出: trainable params: 41M || all params: 8B || trainable%: 0.5%
```

---

## 9.4 QLoRA

### 9.4.1 什么是 QLoRA？

QLoRA = Quantization + LoRA，在 LoRA 的基础上引入量化技术，进一步降低显存需求。

```
┌─────────────────────────────────────────────────────────────┐
│                      QLoRA 流程                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 量化基础模型                                             │
│     Float16 → NF4 (4-bit NormalFloat)                      │
│     模型从 16B × 2B = 32GB → 16B × 0.5B = 8GB            │
│                                                              │
│  2. LoRA 微调                                               │
│     仅更新 LoRA 参数（少量 BF16）                           │
│                                                              │
│  3. 推理时合并                                              │
│     W_new = W_quantized + LoRA                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 9.4.2 QLoRA 代码

```python
from transformers import BitsAndBytesConfig
from peft import prepare_model_for_kbit_training

# 4-bit 量化配置
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",       # NF4 量化
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,  # 双重量化
)

# 加载量化模型
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3-70B",
    quantization_config=bnb_config,
    device_map="auto"
)

# 准备 k-bit 训练
model = prepare_model_for_kbit_training(model)

# 应用 LoRA
model = get_peft_model(model, lora_config)
```

---

## 9.5 LoRA 实战配置

### 9.5.1 常见配置

| 模型规模 | 推荐 r | 目标模块 | 显存占用 |
|---------|--------|---------|---------|
| 7B | 8-16 | q_proj, v_proj | ~8GB |
| 13B | 8-16 | q_proj, v_proj | ~16GB |
| 70B | 16-32 | q_proj, v_proj | ~48GB |

### 9.5.2 训练超参数

```python
training_args = TrainingArguments(
    output_dir="./output",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,      # 累积步数
    learning_rate=2e-4,              # LoRA 常用较高学习率
    num_train_epochs=3,
    fp16=False,
    bf16=True,                        # A100/H100 推荐
    logging_steps=10,
    save_strategy="epoch",
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
)
```

---

## 9.6 LoRA 的变体

### 9.6.1 AdaLoRA

自适应调整不同层的 LoRA 秩：

```python
# 不同层使用不同秩
layer_ranks = {
    "q_proj": 16,
    "k_proj": 8,
    "v_proj": 16,
    "o_proj": 4
}
```

### 9.6.2 QLoRA / LoftQ

结合量化的 LoRA：

```python
# LoftQ: 量化 + 低秩适配
from peft import LoftQConfig

loftq_config = LoftQConfig(quantization_config=bnb_config)
```

### 9.6.3 DoRA

Weight-Decomposed LoRA，将权重更新分解为幅度和方向：

```python
# DoRA 在某些任务上效果更好
lora_config = LoraConfig(..., use_dora=True)
```

---

## 9.7 面试高频问题

### Q1: LoRA 的原理是什么？

> LoRA 基于"低内在秩"假设，假设预训练模型在微调时权重更新具有低秩结构。通过将权重更新 ΔW 分解为两个低秩矩阵 B×A，在保持原权重冻结的同时，只训练这两个小矩阵。

### Q2: LoRA 为什么能省显存？

> 1）原模型权重冻结不更新，无需存储梯度/优化器状态；2）LoRA 参数本身很少（通常 <1% 原模型）；3）可以使用梯度检查点、量化等技术进一步降低。

### Q3: LoRA 的秩 r 怎么选？

> r=4-8：极低资源，通用场景
> r=16-32：平衡性能和效率
> r=64-128：追求更高性能，数据充足
> 通常建议 r ≥ 8，α = 2r

### Q4: LoRA 相比全参数微调会损失性能吗？

> 在大多数任务上，LoRA 可以达到接近全参数微调的效果（通常差距 <2%）。但对于某些需要大幅度修改模型行为的任务，全参数微调可能更好。

### Q5: QLoRA 是什么？

> QLoRA = Quantization + LoRA。将量化（4-bit NF4）和 LoRA 结合，在极低显存下（如单卡 24GB）微调大模型（如 70B）。

---

*参考文献*
- Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models", 2021
- Dettmers et al., "QLoRA: Efficient Finetuning of Quantized LLMs", 2023
