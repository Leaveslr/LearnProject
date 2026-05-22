---
type: note
status: literature
created: 2026-05-19
source: https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf
paper: ../paper/DeepSeek_V4.pdf
tags:
  - AI
  - LLM
  - DeepSeek
  - long-context
  - MoE
  - paper
---

# DeepSeek-V4 技术笔记

一句话：
DeepSeek-V4 的核心不是只把模型做大，而是围绕百万 token 上下文重做注意力、KV cache、训练和后训练基础设施，让长上下文推理和 agent 任务更接近可常态化部署。

## 本地资料

- PDF：[[DeepSeek_V4.pdf|本地 PDF]]
- 官方来源：https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf
- 模型集合：https://huggingface.co/collections/deepseek-ai/deepseek-v4

## 基本信息

- 标题：DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence
- 机构：DeepSeek-AI
- 模型：
  - DeepSeek-V4-Pro：1.6T 总参数，49B 激活参数。
  - DeepSeek-V4-Flash：284B 总参数，13B 激活参数。
- 上下文长度：两者都支持 1M token。
- 预训练数据：Flash 约 32T tokens，Pro 约 33T tokens。
- 主要改动：CSA/HCA 混合注意力、mHC 超连接、Muon 优化器、长上下文 KV cache 与推理基础设施、OPD 后训练。

## 论文想解决的问题

推理模型的 test-time scaling 依赖更长的思考、更长的工具链和更复杂的上下文，但标准 attention 的计算和 KV cache 会随上下文长度急剧膨胀。DeepSeek-V4 的目标是把 1M token 从“可以做 demo”推进到“可以常规使用”，尤其面向长文档分析、多轮 agent、搜索增强问答、代码 agent 和未来在线学习。

## 架构主线

DeepSeek-V4 继承了 DeepSeek-V3 的 MoE 和 MTP 思路，但注意力层和残差路径变化很大。

### 1. Hybrid Attention：CSA + HCA

DeepSeek-V4 用两类压缩注意力交替组成 hybrid attention：

- CSA，Compressed Sparse Attention：先把每 `m=4` 个 token 的 KV 压缩成一个条目，再用 lightning indexer 做 top-k 稀疏选择。Flash 的 top-k 是 512，Pro 的 top-k 是 1024。
- HCA，Heavily Compressed Attention：用更激进的压缩率 `m'=128`，把长序列 KV 大幅压缩，但不再做稀疏 top-k，而是在压缩后的 KV 上做密集注意力。
- 两者都会额外保留一个 sliding window 分支，窗口大小为 128，用来补偿压缩注意力对近邻细粒度依赖的损失。

我的理解：
CSA 负责“从很长历史里挑相关块”，HCA 负责“用极便宜的方式保留全局背景”。Sliding window 则兜住局部语言建模质量。三者组合后，长上下文不是靠单一稀疏策略硬撑，而是把近邻、相关远程块、全局粗粒度记忆拆成不同通道。

### 2. KV cache 效率

论文给出的关键效率结果是：在 1M 上下文下，DeepSeek-V4-Pro 相比 DeepSeek-V3.2 只需要约 27% 的单 token 推理 FLOPs 和约 10% 的 KV cache。相对常见 BF16 GQA8 attention 配置，V4 的 KV cache 在 1M 场景可降到约 2%。

几个实现细节很关键：

- KV 存储混合精度：RoPE 维度用 BF16，其余维度用 FP8。
- CSA 的 indexer attention 使用 FP4。
- 推理侧为 CSA、HCA、SWA 设计异构 KV cache 布局。
- 对共享前缀请求提供 on-disk KV cache，减少重复 prefill。

这说明 DeepSeek-V4 的长上下文能力不是单纯训练出来的，而是架构、精度、缓存布局、kernel 和存储策略一起做出来的。

### 3. mHC：替代普通残差连接

mHC，全称 Manifold-Constrained Hyper-Connections，用多个 residual stream 代替单一路径，并用双随机矩阵约束 residual mapping。这个约束让映射的谱范数不超过 1，目标是让很深网络里的信号传播更稳定。

我的理解：
mHC 是给超大 MoE 模型增加一个新的“宽度/路径”扩展轴。它不直接扩大 hidden size，而是在残差通路上做多流混合。论文强调它解决了普通 Hyper-Connections 在深层堆叠时容易数值不稳定的问题。

### 4. MoE 与 Hash routing

V4 继续使用 DeepSeekMoE：细粒度 routed experts + shared experts，并继续采用 auxiliary-loss-free load balancing。和 V3 相比，V4 做了几处调整：

- affinity score 激活从 Sigmoid 改为 `sqrt(softplus)`。
- 所有 Transformer block 都使用 MoE。
- 前 3 个 MoE 层使用 Hash routing，根据 token id 的哈希函数分配 expert。
- 每个 token 激活 6 个 routed experts。

Pro 的 MoE 配置是 1 个 shared expert + 384 个 routed experts；Flash 是 1 个 shared expert + 256 个 routed experts。

## 训练方法

### 1. Muon 优化器

DeepSeek-V4 大部分参数使用 Muon，embedding、prediction head、RMSNorm 等仍使用 AdamW。论文认为 Muon 带来更快收敛和更好的训练稳定性。Muon 中用 hybrid Newton-Schulz iterations 做近似正交化，并复用 AdamW 的学习率尺度。

### 2. 长上下文 curriculum

训练从 4K 序列长度开始，逐步扩展到 16K、64K 和 1M。前期先用 dense attention warmup，再在 64K 阶段引入 sparse attention，并单独 warmup CSA 的 lightning indexer。

这个节奏很重要：模型不是一开始就直接吃 1M sparse attention，而是先学稳定语言建模，再逐步把长上下文机制接进来。

### 3. 稳定性技巧

论文提到训练 trillion-parameter MoE 时遇到 loss spike，主要和 MoE 层 outlier 以及 routing 相关。两个实用修复：

- Anticipatory Routing：用历史参数提前计算 routing index，打破 backbone 和 routing 同步更新导致的不稳定循环；出现 spike 时动态启用。
- SwiGLU Clamping：对 SwiGLU 的线性分量和门控分量做数值截断，抑制 outlier。

## 后训练

DeepSeek-V4 的后训练和 V3.2 相比，一个关键变化是把 mixed RL 阶段替换成 On-Policy Distillation。

### 1. 三种 reasoning effort

论文定义了三种推理模式：

- Non-think：低延迟、直觉式回答，适合日常任务。
- Think High：显式逻辑分析，适合复杂问题和规划。
- Think Max：最大推理努力，用更长上下文和更弱长度惩罚探索能力边界。

Think Max 不是只调采样参数，而是在 RL 训练阶段就使用不同上下文窗口、长度惩罚和特殊系统提示。

### 2. OPD：多教师 on-policy 蒸馏

DeepSeek-V4 先训练多个领域专家模型，再用 multi-teacher On-Policy Distillation 把能力合并到一个学生模型。论文强调使用 full-vocabulary logit distillation，而不是只在采样 token 上估计 KL，因为后者梯度方差更大、更容易不稳定。

工程上，为了让十多个 trillion 级 teacher 可用，V4 做了：

- teacher 权重集中存储，按需加载；
- 缓存 teacher 最后一层 hidden states，而不是直接落盘完整 logits；
- 训练时按 teacher index 调度样本，减少 prediction head 的加载压力；
- 用专门 TileLang kernel 计算 KL。

### 3. FP4 QAT

后训练阶段引入 FP4 量化感知训练，主要覆盖两类对象：

- MoE expert weights，降低显存和访存压力。
- CSA indexer 的 QK 路径，加速长上下文 attention score 计算。

论文还把 index scores 从 FP32 量化到 BF16，报告称 top-k selector 获得 2 倍加速，同时保持 99.7% KV 条目召回率。

## 基础设施亮点

- Expert parallelism：把 MoE 中 dispatch、linear、activation、combine 细粒度融合成流水化 kernel，让通信被计算隐藏。
- TileLang：用 DSL 平衡 kernel 开发效率和运行效率。
- batch-invariant deterministic kernel：训练和推理保持 batch 不变性和确定性，方便复现、回滚和容错。
- tensor-level activation checkpointing：以张量粒度标注重算，兼顾内存和开发效率。
- preemptible rollout service：用 token 粒度 WAL 和 KV cache 保存，支持 RL/OPD rollout 在抢占和硬件错误后恢复。
- DSec sandbox：为 agentic AI 后训练和评估提供统一沙箱，支持 function call、container、microVM、fullVM。

## 实验结论

Base 模型对比中，DeepSeek-V4-Flash-Base 虽然参数更小，但在多数评测上超过 DeepSeek-V3.2-Base；DeepSeek-V4-Pro-Base 则在知识、推理、代码和长上下文上进一步提升。

后训练模型中，DeepSeek-V4-Pro-Max 是论文主推的最强模式：

- 知识与推理：SimpleQA Verified、HLE、Apex Shortlist 等指标接近或超过部分闭源强模型。
- 代码与 agent：SWE Verified 为 80.6%，Terminal Bench 2.0 为 67.9%，内部 R&D coding benchmark 上接近 Claude Opus 4.5。
- 长上下文：MRCR 在 1M token 下仍保持可用检索能力，CorpusQA 这类更接近真实场景的任务中也有优势。
- 中文写作与企业任务：在 DeepSeek 内部评估中，DeepSeek-V4-Pro 在中文写作、搜索、白领任务上表现强，但格式美观、极端复杂指令跟随、长文压缩仍有改进空间。

## 我的判断

DeepSeek-V4 最值得关注的地方有三个。

第一，它把“百万上下文”从模型能力问题拆成系统工程问题。CSA/HCA 解决注意力复杂度，KV cache layout 解决推理状态管理，on-disk cache 解决共享前缀，RL/OPD 框架解决长 rollout。这种组合比单点的 long-context benchmark 更有参考价值。

第二，V4 的路线对 agent 很友好。长上下文、低 KV cache、Quick Instruction、DSec sandbox、OPD 合并专家能力，都是为复杂工具链和多轮任务服务的。它不是只优化聊天模型，而是在往 agent runtime 和训练闭环靠。

第三，论文也暴露了开放问题：压缩注意力会不会损失某些细粒度远程信息；Think Max 的成本和延迟如何商品化；OPD 多教师体系的迭代成本是否会越来越高；以及长上下文下“找得到”和“用得对”之间还有多少差距。

## 可借鉴点

- 做长上下文系统时，不能只看窗口长度，要同时算单 token FLOPs、KV cache、prefill 复用和 cache 命中后的恢复成本。
- agent 模型评估应加入真实工具环境，单纯标准 benchmark 不够。
- 如果要做领域专家合并，OPD 比权重合并或混合 RL 更值得关注，尤其是 full-vocabulary logit distillation 的稳定性优势。
- 对工程落地来说，Quick Instruction 很实用：把搜索判断、query 生成、领域识别等辅助任务做成特殊 token，复用主模型 KV cache，减少额外小模型和重复 prefill。

## 相关

- [[DeepSeek_V4.pdf]]
