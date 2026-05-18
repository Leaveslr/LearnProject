# PEFT 高效微调技术详解

## PEFT 概述

### 什么是 PEFT？

PEFT（Parameter-Efficient Fine-Tuning，参数高效微调）通过只更新少量参数来实现模型适配，而不是训练所有参数。

```
┌─────────────────────────────────────────────────────────────┐
│                    PEFT vs 全参数微调                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  全参数微调:                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 预训练权重 (全部冻结)  |  全部更新  →  100% 参数   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  PEFT:                                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 预训练权重 (冻结)  |  新增适配器  →  < 1% 参数      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 主要 PEFT 方法

### 1. LoRA (Low-Rank Adaptation)

最流行的 PEFT 方法，通过低秩矩阵近似权重更新：

```
ΔW = B × A, 其中 B ∈ R^(d×r), A ∈ R^(r×k), r << min(d,k)
```

```python
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
)
model = get_peft_model(base_model, config)
```

### 2. QLoRA (Quantized LoRA)

量化 + LoRA，单卡可微调 70B 模型：

```python
# 4-bit 量化 + LoRA
from transformers import BitsAndBytesConfig

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3-70B",
    quantization_config=quant_config,
)
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)
```

### 3. Adapter Tuning

在 Transformer 层之间插入适配器模块：

```
┌────────────────────────────────────────────────────────────┐
│                  Adapter Tuning 结构                         │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  Input                                                       │
│    │                                                        │
│    ▼                                                        │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Adapter:  DownProj → Non-linear → UpProj          │    │
│  │           (d → r)    SiLU      (r → d)            │    │
│  └────────────────────────────────────────────────────┘    │
│    │                                                        │
│    ▼                                                        │
│  LayerNorm ──→ + ──→ Output                                │
│                  ▲                                         │
│                  │                                         │
│              残差连接                                        │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

### 4. Prefix Tuning

在输入前添加可学习的前缀：

```
┌────────────────────────────────────────────────────────────┐
│                    Prefix Tuning                            │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  可学习前缀 (Virtual Tokens)                                │
│  ┌─────┬─────┬─────┬─────────────────────────────────┐    │
│  │ P_1 │ P_2 │ ... │ 真实输入: "如何学习大模型？"     │    │
│  └─────┴─────┴─────┴─────────────────────────────────┘    │
│  ↑ 冻结预训练权重，只训练 P_1, P_2, ...                  │
│                                                              │
│  与 Prompt Tuning 的区别:                                   │
│  - Prompt Tuning: 只在 Embedding 层添加                     │
│  - Prefix Tuning: 每层都添加可学习前缀                       │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

### 5. P-Tuning / P-Tuning v2

使用连续提示而不是离散 token：

```python
from peft import PromptTuningConfig, get_peft_model

config = PromptTuningConfig(
    task_type="CAUSAL_LM",
    num_virtual_tokens=20,  # 20 个虚拟 token
    prompt_tuning_init="TEXT",
    prompt_tuning_init_text="根据以下问题给出专业回答:",
)
model = get_peft_model(base_model, config)
```

## PEFT 方法对比

| 方法 | 可训练参数 | 推理开销 | 效果 | 实现复杂度 |
|------|-----------|---------|------|-----------|
| **LoRA** | < 1% | 无 | 优秀 | 低 |
| **QLoRA** | < 0.5% | 无 | 良好 | 中 |
| **Adapter** | 1-5% | 有 | 良好 | 中 |
| **Prefix Tuning** | < 1% | 无 | 良好 | 中 |
| **P-Tuning** | < 1% | 无 | 一般 | 低 |

## 选择指南

```
┌─────────────────────────────────────────────────────────────┐
│                    PEFT 方法选择树                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  需要多任务切换? ──→ LoRA (推荐, 权重可独立保存)             │
│      │                                                       │
│      否                                                      │
│      │                                                       │
│      ▼                                                       │
│  显存极度受限? ──→ QLoRA (单卡 24GB 可跑 70B)               │
│      │                                                       │
│      否                                                      │
│      │                                                       │
│      ▼                                                       │
│  需要无推理开销? ──→ LoRA / Prefix Tuning                   │
│      │                                                       │
│      否                                                      │
│      │                                                       │
│      ▼                                                       │
│  Adapter Tuning (通用)                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 面试要点

1. **LoRA 最常用**：实现简单，效果好，权重可切换
2. **QLoRA**：量化+LoRA，适合资源受限场景
3. **Adapter**：插入式设计，但有推理开销
4. **Prefix/P-Tuning**：不用修改模型结构，但调优困难

