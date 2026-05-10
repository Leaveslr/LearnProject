---
type: note
status: literature
created: 2026-05-10
source: https://arxiv.org/abs/2605.06507
paper: ../Papers/MARBLE Multi-Aspect Reward Balance for Diffusion RL.pdf
tags:
  - AI
  - diffusion
  - reinforcement-learning
  - alignment
  - paper
---

# MARBLE Multi-Aspect Reward Balance for Diffusion RL

一句话：
MARBLE 在梯度空间平衡多个图像奖励，让扩散模型 RL 微调不再依赖手工调 reward 权重。

## 本地资料

- PDF：[[MARBLE Multi-Aspect Reward Balance for Diffusion RL.pdf|本地 PDF]]
- arXiv：https://arxiv.org/abs/2605.06507
- Hugging Face：https://huggingface.co/papers/2605.06507
- 项目页：https://aim-uofa.github.io/MARBLE

## 核心问题

- 扩散模型对齐通常要同时优化多个目标，例如美学、文本一致性、人类偏好、安全性或其他图像质量指标。
- 常见做法是把多个 reward 加权求和，或者按阶段手工切换训练目标。
- 加权求和的问题在于，不同 rollout 往往只对某些 reward 维度有信息量，对其他维度噪声很大。
- 直接相加会稀释有效监督，甚至让某些 reward 的梯度方向互相冲突。

## 方法

MARBLE 的核心思路是从 reward-sum 转向 gradient balancing：

- 为每个 reward 维护独立 advantage estimator。
- 分别计算每个 reward 对应的 policy gradient。
- 通过二次规划把多个梯度合成为一个统一更新方向。
- 不需要手工设定 reward 权重。
- 结合 DiffusionNFT 损失的仿射结构，把原本接近 K+1 次 backward 的成本摊销到接近单 reward baseline。
- 用 EMA 平滑 balancing coefficients，减少单个 batch 的短期波动。

## 实验结果

- 在 SD3.5 Medium 上同时优化 5 个 reward，MARBLE 能让 5 个维度一起提升。
- 加权求和下，最差 reward 的梯度余弦在 80% mini-batch 中为负；MARBLE 能把它稳定转为正向。
- 训练速度达到 baseline 的 0.97X，接近单 reward 训练成本。

## 我的理解

MARBLE 解决的是多目标对齐里非常实际的痛点：reward 多了以后，真正困难的不是有没有指标，而是如何让这些指标同时产生有效训练信号。

加权求和看起来简单，但它默认每个样本对所有 reward 都同样有意义。图像生成里这个假设通常不成立：一个样本可能很好地暴露审美问题，却对文本对齐没有太多信息。MARBLE 把问题放到梯度空间处理，更接近“每个目标先表达自己的更新诉求，再协商一个共同方向”。

这篇论文对扩散模型有直接价值，也可以启发 LLM 多 reward RL：当 reward 维度之间互相冲突时，先分开估计 advantage 和梯度，再做方向协调，可能比调权重更稳。

## 可借鉴点

- 多 reward 训练不要急着做 scalarization，可以先检查不同 reward 的梯度方向是否冲突。
- reward 权重不是唯一控制手段，梯度空间的投影、约束和合成也可以作为对齐方法。
- 对生产系统里的偏好对齐，MARBLE 这类方法适合用在“既要质量、又要安全、还要遵循指令”的多目标场景。

## 相关

- [[Self-Evolving AI Agents Survey]]
