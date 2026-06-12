# 第五章：RLHF 与对齐技术

## 5.1 什么是对齐（Alignment）？

### 5.1.1 对齐问题

预训练模型学习的是**预测下一个 token**，而不是**遵循人类指令**。

```
预训练模型：
  输入: "如何制作炸弹？"
  输出: "以下是制作方法..."（有害但概率最高）

对齐后模型：
  输入: "如何制作炸弹？"
  输出: "抱歉，我无法帮助这个请求。"
```

### 5.1.2 对齐的目标

1. **有用 (Helpful)**：遵循用户指令
2. **无害 (Harmless)**：拒绝有害请求
3. **诚实 (Honest)**：不产生幻觉，提供准确信息

---

## 5.2 RLHF 概述

### 5.2.1 RLHF 流程

```
┌─────────────────────────────────────────────────────────────┐
│                    RLHF 三阶段流程                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  阶段1: 监督微调 (SFT)                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  人类示范 → 收集高质量问答对 → 有监督微调预训练模型      │   │
│  └─────────────────────────────────────────────────────┘   │
│                         ↓                                   │
│  阶段2: 奖励模型 (RM)                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  收集比较数据 → 训练奖励模型预测人类偏好               │   │
│  │  输入x + 回答y → 奖励分数r(x,y)                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                         ↓                                   │
│  阶段3: PPO 强化学习                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  使用奖励模型 → PPO 算法优化策略模型                   │   │
│  │  最大化期望奖励 + KL 约束防止偏离太远                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2.2 为什么需要 RLHF？

| 方法 | 优点 | 缺点 |
|------|------|------|
| **纯 SFT** | 简单、稳定 | 需要大量人工标注、难以覆盖所有场景 |
| **RLHF** | 泛化强、可利用偏好信号 | 复杂、训练不稳定 |

---

## 5.3 PPO 算法详解

### 5.3.1 PPO 核心公式

PPO（Proximal Policy Optimization）的目标函数：

```
L^CLIP(θ) = E_t [ min(r_t(θ) * A_t, clip(r_t(θ), 1-ε, 1+ε) * A_t) ]
```

其中：
- r_t(θ) = π_θ(a_t|s_t) / π_old(a_t|s_t)  （重要性采样比率）
- A_t = 优势函数（Advantage）
- ε = 裁剪参数（通常 0.1-0.2）

### 5.3.2 KL 散度约束

防止策略更新过大导致性能崩溃：

```
L_total = L_RLHF + β * KL(π_θ || π_ref)
```

其中 π_ref 是 SFT 阶段的参考模型。

---

## 5.4 DPO（Direct Preference Optimization）

### 5.4.1 DPO 的核心思想

DPO 绕过显式奖励模型，直接使用偏好对优化策略：

```
RLHF:  偏好数据 → 奖励模型 → PPO → 策略模型
DPO:    偏好数据 → 直接优化策略模型
```

### 5.4.2 DPO 公式

对于偏好数据 (x, y_w, y_l)：
- x: 输入 prompt
- y_w: 人类偏好回答
- y_l: 人类不偏好回答

**DPO 损失函数**：

```
L_DPO = -E_(x,y_w,y_l) [ log σ( β * [log(π_θ(y_w|x)/π_ref(y_w|x)) - log(π_θ(y_l|x)/π_ref(y_l|x))] ) ]
```

```python
import torch
import torch.nn.functional as F

def dpo_loss(
    policy_model, ref_model,  # 策略模型和参考模型
    prompt_ids, chosen_ids, rejected_ids,  # token ids
    beta=0.1  # 温度参数
):
    # 计算 log π_θ(y|x) 和 log π_ref(y|x)
    chosen_logp = get_log_probs(policy_model, prompt_ids, chosen_ids)
    rejected_logp = get_log_probs(policy_model, prompt_ids, rejected_ids)
    
    with torch.no_grad():
        ref_chosen_logp = get_log_probs(ref_model, prompt_ids, chosen_ids)
        ref_rejected_logp = get_log_probs(ref_model, prompt_ids, rejected_ids)
    
    # DPO loss
    logits = beta * (
        (chosen_logp - ref_chosen_logp) - 
        (rejected_logp - ref_rejected_logp)
    )
    loss = -F.logsigmoid(logits).mean()
    return loss
```

### 5.4.3 DPO vs RLHF

| 特性 | RLHF | DPO |
|------|------|-----|
| **奖励模型** | 需要单独训练 | 不需要 |
| **训练复杂度** | 高（PPO 多步骤） | 低（单步） |
| **显存需求** | 大（需要价值网络） | 小 |
| **稳定性** | 可能不稳定 | 更稳定 |
| **超参数** | 多（PPO 多个） | 少（主要 β） |

---

## 5.5 GRPO（Group Relative Policy Optimization）

### 5.5.1 GRPO 核心思想

DeepSeek 提出的方法，对同一 prompt 采样多个响应，使用组内相对奖励计算优势：

```
PPO:   需要单独的价值网络（Critic）估计优势
GRPO:  同一 prompt 采样 G 个响应，用组内均值/标准差归一化
```

### 5.5.2 GRPO 代码示例

```python
import torch

G = 4  # Group 数量
epsilon = 0.2  # PPO 截断参数
beta = 0.01  # KL 惩罚系数

for epoch in range(num_epochs):
    # 1. 组采样
    generated_outputs = [
        policy_model.generate(prompt, do_sample=True, temperature=0.8) 
        for _ in range(G)
    ]
    
    # 2. 计算奖励
    rewards = [reward_function(y, expected_y) for y in generated_outputs]
    rewards_tensor = torch.tensor(rewards)
    
    # 3. 计算相对优势（替代价值网络）
    mean_reward = rewards_tensor.mean()
    std_reward = rewards_tensor.std() + 1e-8
    advantages = (rewards_tensor - mean_reward) / std_reward
    
    # 4. GRPO 损失
    loss = 0
    for i in range(G):
        log_prob_policy = get_log_probs(policy_model, prompt, generated_outputs[i])
        with torch.no_grad():
            log_prob_ref = get_log_probs(ref_model, prompt, generated_outputs[i])
        
        # 重要性采样比率
        ratio = torch.exp(log_prob_policy - log_prob_ref.detach())
        
        # PPO 截断目标
        surr1 = ratio * advantages[i]
        surr2 = torch.clamp(ratio, 1.0 - epsilon, 1.0 + epsilon) * advantages[i]
        policy_loss = -torch.min(surr1, surr2)
        
        # KL 惩罚
        kl_div = log_prob_ref - log_prob_policy
        
        loss += policy_loss + beta * kl_div
    
    loss = loss / G
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
```

---

## 5.6 面试高频问题

### Q1: 什么是 RLHF？为什么需要它？

> RLHF（Reinforcement Learning from Human Feedback）是一种让模型学习符合人类偏好的技术。通过收集人类对不同回答的比较数据，训练奖励模型，然后使用强化学习优化策略，使模型产生人类更喜欢的输出。

### Q2: PPO 和 DPO 有什么区别？

> PPO 是传统 RLHF 的核心算法，需要单独训练奖励模型和价值网络。DPO 是一种更简单的方法，直接用偏好对优化策略，不需要显式奖励模型，训练更稳定。

### Q3: 为什么 DPO 比 RLHF 更简单？

> DPO 将 RLHF 的多阶段流程（奖励模型 + PPO）简化为单步策略优化。它通过重参数化技巧，直接从偏好数据学习，避免了强化学习的不稳定性。

### Q4: GRPO 相比 PPO 有什么优势？

> GRPO 不需要单独的价值网络（Critic），用组内采样的相对奖励计算优势，降低了计算开销和实现复杂度。

### Q5: 什么是对齐税（Alignment Tax）？

> 对齐训练可能导致模型在某些任务上的能力下降（如数学、代码）。这是因为模型被约束生成"安全"但可能"保守"的回答。

---

*参考文献*
- Ouyang et al., "Training language models to follow instructions with human feedback", 2022
- Rafailov et al., "Direct Preference Optimization: Your Language Model is Secretly a Reward Model", 2023
- DeepSeek, "DeepSeek-R1", 2025
