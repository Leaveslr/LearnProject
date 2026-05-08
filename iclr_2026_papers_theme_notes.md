# ICLR 2026 主会论文主题整理

来源: https://iclr.cc/virtual/2026/papers.html

整理时间: 2026-05-06

页面解析结果: 从 ICLR 2026 virtual papers 页面提取到 5468 篇论文标题。下面的主题分类基于标题关键词做快速归纳；同一篇论文可能同时属于多个主题，因此各主题数量不是互斥统计。

## 总览

ICLR 2026 主会论文的高频方向非常集中在几个大块:

1. LLM、Agent、post-training、reward/preference alignment
2. reasoning、数学、代码、verifier 与 chain-of-thought
3. diffusion、flow、image/video/audio generation
4. VLM、多模态、视频理解、音频视觉联合建模
5. RL、机器人、control、planning、offline RL
6. vision、3D、detection、segmentation、scene generation
7. transformer/attention/optimization/scaling law/theory
8. dataset、benchmark、quantization、distillation、inference efficiency
9. safety、robustness、privacy、unlearning、jailbreak、bias
10. scientific ML、bio/medical、protein、molecule、weather/climate

## 主题 1: LLM / Agent / Post-training

命中数量: 1761

关键词: LLM, language model, agent, post-training, fine-tuning, preference, reward model, RLHF, instruction, prompt, tool, memory。

代表论文:

1. [ChatInject: Abusing Chat Templates for Prompt Injection in LLM Agents](https://iclr.cc/virtual/2026/poster/10009048)
2. [Towards Understanding Valuable Preference Data for Large Language Model Alignment](https://iclr.cc/virtual/2026/poster/10010595)
3. [Chasing the Tail: Effective Rubric-based Reward Modeling for Large Language Model Post-Training](https://iclr.cc/virtual/2026/poster/10007351)
4. [Prompt-MII: Meta-Learning Instruction Induction for LLMs](https://iclr.cc/virtual/2026/poster/10006473)
5. [Prompt Curriculum Learning for Efficient LLM Post-Training](https://iclr.cc/virtual/2026/poster/10006420)
6. [Data Selection for LLM Alignment Using Fine-Grained Preferences](https://iclr.cc/virtual/2026/poster/10007475)
7. [Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions](https://iclr.cc/virtual/2026/poster/10010781)
8. [GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs](https://iclr.cc/virtual/2026/poster/10008792)
9. [MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent](https://iclr.cc/virtual/2026/poster/10007825)
10. [Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization](https://iclr.cc/virtual/2026/poster/10009229)

阅读提示: 这个方向可以重点看 agent memory、post-training 数据选择、reward modeling，以及 prompt/template 安全。它和 RSI workshop 的 agent 自我改进主题高度重叠。

## 主题 2: Reasoning / Math / Code

命中数量: 713

关键词: reasoning, chain-of-thought, math, theorem, proof, code, program, symbolic, logic, verifier。

代表论文:

1. [VeriCoT: Neuro-symbolic Chain-of-Thought Validation via Logical Consistency Checks](https://iclr.cc/virtual/2026/poster/10006464)
2. [MAD-Logic: Multi-Agent Debate Enhances Symbolic Translation and Reasoning](https://iclr.cc/virtual/2026/poster/10007131)
3. [SceneCOT: Eliciting Grounded Chain-of-Thought Reasoning in 3D Scenes](https://iclr.cc/virtual/2026/poster/10009257)
4. [Uni-CoT: Towards Unified Chain-of-Thought Reasoning Across Text and Vision](https://iclr.cc/virtual/2026/poster/10011423)
5. [CoT-Evo: Evolutionary Distillation of Chain-of-Thought for Scientific Reasoning](https://iclr.cc/virtual/2026/poster/10009790)
6. [FaithCoT-Bench: Benchmarking Instance-Level Faithfulness of Chain-of-Thought Reasoning](https://iclr.cc/virtual/2026/poster/10007686)
7. [The Natural Geometry of Code: Hyperbolic Representation Learning for Program Reasoning](https://iclr.cc/virtual/2026/poster/10007369)
8. [Reinforcing General Reasoning Without Verifiers](https://iclr.cc/virtual/2026/poster/10007455)
9. [Verifying Chain-of-Thought Reasoning via Its Computational Graph](https://iclr.cc/virtual/2026/poster/10010813)
10. [Hilbert: Recursively Building Formal Proofs with Informal Reasoning](https://iclr.cc/virtual/2026/poster/10010497)

阅读提示: 这组论文的主线是“让推理可验证、可迁移、可跨模态”。如果关心 LLM reasoning，可以从 CoT faithfulness、verifier-free RL、formal proof 这几条切入。

## 主题 3: Generative Models / Diffusion / Flow

命中数量: 981

关键词: diffusion, flow, generative, generation, denoising, score, image/video generation, text-to-image。

代表论文:

1. [Asynchronous Denoising Diffusion Models for Aligning Text-to-Image Generation](https://iclr.cc/virtual/2026/poster/10008820)
2. [Interleaving Reasoning for Better Text-to-Image Generation](https://iclr.cc/virtual/2026/poster/10007687)
3. [Object Fidelity Diffusion for Remote Sensing Image Generation](https://iclr.cc/virtual/2026/poster/10007462)
4. [Neodragon: Mobile Video Generation Using Diffusion Transformer](https://iclr.cc/virtual/2026/poster/10008995)
5. [Uniform Discrete Diffusion with Metric Path for Video Generation](https://iclr.cc/virtual/2026/poster/10010514)
6. [Consistent Text-to-Image Generation via Scene De-Contextualization](https://iclr.cc/virtual/2026/poster/10007146)
7. [CoDi: Subject-Consistent and Pose-Diverse Text-to-Image Generation](https://iclr.cc/virtual/2026/poster/10011174)
8. [Long-Text-to-Image Generation via Compositional Prompt Decomposition](https://iclr.cc/virtual/2026/poster/10007837)
9. [Syncphony: Synchronized Audio-to-Video Generation with Diffusion Transformers](https://iclr.cc/virtual/2026/poster/10007074)
10. [SANA-Video: Efficient Video Generation with Block Linear Diffusion Transformer](https://iclr.cc/virtual/2026/poster/10007520)

阅读提示: 生成模型方向继续向长 prompt、主体一致性、视频生成、音画同步、评估与效率推进。

## 主题 4: Multimodal / VLM / Video / Audio

命中数量: 660

关键词: vision-language, multimodal, VLM, video, audio, speech, image-text, caption, OCR。

代表论文:

1. [AVoCaDO: An Audiovisual Video Captioner Driven by Temporal Orchestration](https://iclr.cc/virtual/2026/poster/10006791)
2. [IF-VidCap: Can Video Caption Models Follow Instructions?](https://iclr.cc/virtual/2026/poster/10007706)
3. [CaReBench: A Fine-grained Benchmark for Video Captioning and Retrieval](https://iclr.cc/virtual/2026/poster/10009770)
4. [GPT4Scene: Understand 3D Scenes from Videos with Vision-Language Models](https://iclr.cc/virtual/2026/poster/10011913)
5. [OmniVideoBench: Towards Audio-Visual Understanding Evaluation for Omni MLLMs](https://iclr.cc/virtual/2026/poster/10010256)
6. [MMR-V: What's Left Unsaid? A Benchmark for Multimodal Deep Reasoning in Videos](https://iclr.cc/virtual/2026/poster/10006623)
7. [WAVE: Learning Unified & Versatile Audio-Visual Embeddings with Multimodal LLM](https://iclr.cc/virtual/2026/poster/10009925)
8. [VideoMathQA: Benchmarking Mathematical Reasoning via Multimodal Understanding in Video](https://iclr.cc/virtual/2026/poster/10009154)
9. [Vid-LLM: A Compact Video-based 3D Multimodal LLM with Reconstruction-Reasoning Synergy](https://iclr.cc/virtual/2026/poster/10007723)
10. [PrismAudio: Decomposed Chain-of-Thought and Multi-dimensional Rewards for Video-to-Audio Generation](https://iclr.cc/virtual/2026/poster/10008525)

阅读提示: 多模态论文的重点不只是“看图说话”，而是视频时序、音画联合、3D 场景理解和多模态推理评测。

## 主题 5: RL / Robotics / Control

命中数量: 901

关键词: reinforcement learning, policy, robot, control, planning, imitation, offline RL, bandit, trajectory, navigation。

代表论文:

1. [Masked Generative Policy for Robotic Control](https://iclr.cc/virtual/2026/poster/10010143)
2. [Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning](https://iclr.cc/virtual/2026/poster/10006732)
3. [Learning Video Generation for Robotic Manipulation with Collaborative Trajectory Control](https://iclr.cc/virtual/2026/poster/10009761)
4. [BridgeDrive: Diffusion Bridge Policy for Closed-Loop Trajectory Planning in Autonomous Driving](https://iclr.cc/virtual/2026/poster/10008420)
5. [Less Is More: Clustered Cross-Covariance Control for Offline RL](https://iclr.cc/virtual/2026/poster/10008379)
6. [Ctrl-World: A Controllable Generative World Model for Robot Manipulation](https://iclr.cc/virtual/2026/poster/10011332)
7. [ExoPredicator: Learning Abstract Models of Dynamic Worlds for Robot Planning](https://iclr.cc/virtual/2026/poster/10008751)
8. [Self-Improving Loops for Visual Robotic Planning](https://iclr.cc/virtual/2026/poster/10009368)
9. [Policy Contrastive Decoding for Robotic Foundation Models](https://iclr.cc/virtual/2026/poster/10009706)
10. [Remotely Detectable Robot Policy Watermarking](https://iclr.cc/virtual/2026/poster/10011170)

阅读提示: 这个方向的明显趋势是把 diffusion/video/world model 接到 control 和 robot planning 上，同时继续处理 offline RL、轨迹选择和策略安全问题。

## 主题 6: Vision / 3D / Perception

命中数量: 816

关键词: segmentation, detection, recognition, image, vision, 3D, point cloud, depth, pose, NeRF, scene, object。

代表论文:

1. [DNOD: Deformable Neural Operators for Object Detection in SAR Images](https://iclr.cc/virtual/2026/poster/10014070)
2. [GOLDILOCS: GENERAL OBJECT-LEVEL DETECTION AND LABELING OF CHANGES IN SCENES](https://iclr.cc/virtual/2026/poster/10007228)
3. [Unbiased Object Detection Beyond Frequency with Visually Prompted Image Synthesis](https://iclr.cc/virtual/2026/poster/10009419)
4. [FSOD-VFM: Few-Shot Object Detection with Vision Foundation Models and Graph Diffusion](https://iclr.cc/virtual/2026/poster/10007893)
5. [GPT4Scene: Understand 3D Scenes from Videos with Vision-Language Models](https://iclr.cc/virtual/2026/poster/10011913)
6. [ComGS: Efficient 3D Object-Scene Composition via Surface Octahedral Probes](https://iclr.cc/virtual/2026/poster/10006547)
7. [Scenethesis: A Language and Vision Agentic Framework for 3D Scene Generation](https://iclr.cc/virtual/2026/poster/10009362)
8. [One2Scene: Geometric Consistent Explorable 3D Scene Generation from a Single Image](https://iclr.cc/virtual/2026/poster/10007985)
9. [DepthLM: Metric Depth from Vision Language Models](https://iclr.cc/virtual/2026/poster/10009767)
10. [Video Scene Segmentation with Genre and Duration Signals](https://iclr.cc/virtual/2026/poster/10008536)

阅读提示: 传统 perception 问题正在被 VFM/VLM、生成式 3D、scene-level reasoning 重塑。

## 主题 7: Theory / Optimization / Architecture

命中数量: 932

关键词: theory, optimization, gradient, transformer, attention, architecture, scaling, generalization, loss, convergence, kernel, GNN。

代表论文:

1. [Critical attention scaling in long-context transformers](https://iclr.cc/virtual/2026/poster/10011299)
2. [Sobolev Gradient Ascent for Optimal Transport: Barycenter Optimization and Convergence Analysis](https://iclr.cc/virtual/2026/poster/10010273)
3. [Scaling Attention via Feature Sparsity](https://iclr.cc/virtual/2026/poster/10009189)
4. [Scaling Laws for Diffusion Transformers](https://iclr.cc/virtual/2026/poster/10009343)
5. [On the Convergence Direction of Gradient Descent](https://iclr.cc/virtual/2026/poster/10011642)
6. [Long-Context Generalization with Sparse Attention](https://iclr.cc/virtual/2026/poster/10009641)
7. [STEM: SCALING TRANSFORMERS WITH EMBEDDING MODULES](https://iclr.cc/virtual/2026/poster/10008106)
8. [Decoupling Positional and Symbolic Attention in Transformers](https://iclr.cc/virtual/2026/poster/10009178)
9. [Scaling Laws Meet Model Architecture: Toward Inference-Efficient LLMs](https://iclr.cc/virtual/2026/poster/10011936)
10. [Taming Curvature: Architecture Warm-up for Stable Transformer Training](https://iclr.cc/virtual/2026/poster/10010735)

阅读提示: 这类论文适合按“long-context attention”“scaling laws”“optimization dynamics”“architecture efficiency”四条线读。

## 主题 8: Data / Efficiency / Systems

命中数量: 996

关键词: data selection, dataset, benchmark, efficient, compression, quantization, distillation, pruning, serving, inference, memory。

代表论文:

1. [Dataset Distillation as Pushforward Optimal Quantization](https://iclr.cc/virtual/2026/poster/10010609)
2. [MARC: Memory-Augmented RL Token Compression for Efficient Video Understanding](https://iclr.cc/virtual/2026/poster/10011432)
3. [The Quest for Efficient Reasoning: A Data-Centric Benchmark to CoT Distillation](https://iclr.cc/virtual/2026/poster/10010734)
4. [ParoQuant: Pairwise Rotation Quantization for Efficient Reasoning LLM Inference](https://iclr.cc/virtual/2026/poster/10011824)
5. [Channel-Aware Mixed-Precision Quantization for Efficient Long-Context Inference](https://iclr.cc/virtual/2026/poster/10006529)
6. [CoDA: From Text-to-Image Diffusion Models to Training-Free Dataset Distillation](https://iclr.cc/virtual/2026/poster/10011340)
7. [GradPruner: Gradient-guided Layer Pruning Enabling Efficient Fine-Tuning and Inference for LLMs](https://iclr.cc/virtual/2026/poster/10008556)
8. [Universal Model Routing for Efficient LLM Inference](https://iclr.cc/virtual/2026/poster/10007775)
9. [Q&C: When Quantization Meets Cache in Efficient Generation](https://iclr.cc/virtual/2026/poster/10011052)
10. [FreeKV: Boosting KV Cache Retrieval for Efficient LLM Inference](https://iclr.cc/virtual/2026/poster/10006722)

阅读提示: 这一组非常适合工程视角阅读，重点关注推理成本、长上下文 KV cache、量化、剪枝、数据蒸馏和 benchmark 设计。

## 主题 9: Safety / Robustness / Privacy / Unlearning

命中数量: 499

关键词: safety, robust, adversarial, privacy, unlearning, bias, fairness, jailbreak, backdoor, poisoning, hallucination。

代表论文:

1. [AdvChain: Adversarial Chain-of-Thought Tuning for Robust Safety Alignment of Large Reasoning Models](https://iclr.cc/virtual/2026/poster/10007590)
2. [FERD: Fairness-Enhanced Data-Free Adversarial Robustness Distillation](https://iclr.cc/virtual/2026/poster/10007897)
3. [Don't Shift the Trigger: Robust Gradient Ascent for Backdoor Unlearning](https://iclr.cc/virtual/2026/poster/10006778)
4. [Reasoned Safety Alignment: Ensuring Jailbreak Defense via Answer-Then-Check](https://iclr.cc/virtual/2026/poster/10010790)
5. [DualEdit: Mitigating Safety Fallback in LLM Backdoor Editing via Affirmation-Refusal Regulation](https://iclr.cc/virtual/2026/poster/10008415)
6. [Self-Jailbreaking: Language Models Can Reason Themselves Out of Safety Alignment After Benign Reasoning Training](https://iclr.cc/virtual/2026/poster/10008673)
7. [Safety Mirage: How Spurious Correlations Undermine VLM Safety Fine-Tuning and Can Be Mitigated by Machine Unlearning](https://iclr.cc/virtual/2026/poster/10009564)
8. [SafeDialBench: A Fine-Grained Safety Evaluation Benchmark for Large Language Models in Multi-Turn Dialogues with Diverse Jailbreak Attacks](https://iclr.cc/virtual/2026/poster/10010144)
9. [Mitigating Privacy Risk via Forget Set-Free Unlearning](https://iclr.cc/virtual/2026/poster/10008442)
10. [Dual-Space Smoothness for Robust and Balanced LLM Unlearning](https://iclr.cc/virtual/2026/poster/10009153)

阅读提示: 安全方向值得重点看 reasoning model 的 jailbreak、VLM safety、unlearning、backdoor editing 和 privacy leakage。

## 主题 10: Scientific ML / Bio / Medical / Climate

命中数量: 168

关键词: protein, medical, clinical, molecule, drug, biology, genomic, chemistry, physics, climate, weather, materials。

代表论文:

1. [Zephyrus: An Agentic Framework for Weather Science](https://iclr.cc/virtual/2026/poster/10008692)
2. [PoseX: AI Defeats Physics-based Methods on Protein Ligand Cross-Docking](https://iclr.cc/virtual/2026/poster/10007208)
3. [DeepPrim: a Physics-Driven 3D Short-term Weather Forecaster via Primitive Equation Learning](https://iclr.cc/virtual/2026/poster/10010631)
4. [MedAgentGym: A Scalable Agentic Training Environment for Code-Centric Reasoning in Biomedical Data Science](https://iclr.cc/virtual/2026/poster/10007894)
5. [UrbanGraph: Physics-Informed Spatio-Temporal Dynamic Heterogeneous Graphs for Urban Microclimate Prediction](https://iclr.cc/virtual/2026/poster/10008471)
6. [KGOT: Unified Knowledge Graph and Optimal Transport Pseudo-Labeling for Molecule-Protein Interaction Prediction](https://iclr.cc/virtual/2026/poster/10009196)
7. [From Medical Records to Diagnostic Dialogues: A Clinical-Grounded Approach and Dataset for Psychiatric Comorbidity](https://iclr.cc/virtual/2026/poster/10007048)
8. [CARE: Towards Clinical Accountability in Multi-Modal Medical Reasoning with an Evidence-Grounded Agentic Framework](https://iclr.cc/virtual/2026/poster/10006707)
9. [Shrinking Proteins with Diffusion](https://iclr.cc/virtual/2026/poster/10007198)
10. [SimpleFold: Folding Proteins is Simpler than You Think](https://iclr.cc/virtual/2026/poster/10011905)

阅读提示: 这个方向值得按“agentic science”“protein/molecule”“clinical reasoning”“weather/climate”四类拆开看。

## 推荐阅读路线

### 路线 A: LLM / Agent / 自我改进

1. Prompt Curriculum Learning for Efficient LLM Post-Training
2. Chasing the Tail: Effective Rubric-based Reward Modeling for Large Language Model Post-Training
3. Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions
4. GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs
5. MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent

适合问题: 如何让 LLM/Agent 变得更会学习、更会记忆、更会长期交互？

### 路线 B: Reasoning / Verifier / CoT

1. VeriCoT: Neuro-symbolic Chain-of-Thought Validation via Logical Consistency Checks
2. FaithCoT-Bench: Benchmarking Instance-Level Faithfulness of Chain-of-Thought Reasoning
3. Reinforcing General Reasoning Without Verifiers
4. Verifying Chain-of-Thought Reasoning via Its Computational Graph
5. Hilbert: Recursively Building Formal Proofs with Informal Reasoning

适合问题: 推理能力如何训练、评估和验证？

### 路线 C: 生成模型与视频

1. Scaling Laws for Diffusion Transformers
2. Interleaving Reasoning for Better Text-to-Image Generation
3. Long-Text-to-Image Generation via Compositional Prompt Decomposition
4. Neodragon: Mobile Video Generation Using Diffusion Transformer
5. SANA-Video: Efficient Video Generation with Block Linear Diffusion Transformer

适合问题: diffusion transformer 如何继续扩展到复杂 prompt、视频和高效生成？

### 路线 D: 多模态推理

1. OmniVideoBench: Towards Audio-Visual Understanding Evaluation for Omni MLLMs
2. MMR-V: What's Left Unsaid? A Benchmark for Multimodal Deep Reasoning in Videos
3. VideoMathQA: Benchmarking Mathematical Reasoning via Multimodal Understanding in Video
4. Vid-LLM: A Compact Video-based 3D Multimodal LLM with Reconstruction-Reasoning Synergy
5. Uni-CoT: Towards Unified Chain-of-Thought Reasoning Across Text and Vision

适合问题: 多模态模型能否真正“推理”，而不仅是识别和描述？

### 路线 E: 机器人与世界模型

1. Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning
2. Learning Video Generation for Robotic Manipulation with Collaborative Trajectory Control
3. Ctrl-World: A Controllable Generative World Model for Robot Manipulation
4. ExoPredicator: Learning Abstract Models of Dynamic Worlds for Robot Planning
5. Self-Improving Loops for Visual Robotic Planning

适合问题: video/world model 如何变成可执行的机器人策略？

### 路线 F: 安全与对齐

1. AdvChain: Adversarial Chain-of-Thought Tuning for Robust Safety Alignment of Large Reasoning Models
2. Reasoned Safety Alignment: Ensuring Jailbreak Defense via Answer-Then-Check
3. Self-Jailbreaking: Language Models Can Reason Themselves Out of Safety Alignment After Benign Reasoning Training
4. Safety Mirage: How Spurious Correlations Undermine VLM Safety Fine-Tuning and Can Be Mitigated by Machine Unlearning
5. SafeDialBench: A Fine-Grained Safety Evaluation Benchmark for Large Language Models in Multi-Turn Dialogues with Diverse Jailbreak Attacks

适合问题: reasoning/post-training 会不会削弱安全边界？如何评估和修复？

## 和 RSI Workshop 的连接

如果把主会论文和 RSI workshop 放在一起看，可以形成几条主线:

1. Agent 自我改进: workshop 更聚焦 recursive self-improvement，主会提供更多 agent memory、post-training、tool/prompt 安全材料。
2. Reasoning 自我训练: workshop 关注 test-time self-improvement 和 self-play，主会有更多 CoT faithfulness、verifier、formal proof、reasoning benchmark。
3. 机器人闭环: workshop 的 VLA/world model 论文可以和主会的 video model for control、generative world model、robot planning 放一起读。
4. 安全治理: workshop 的 reward hacking、tampering、高阶目标风险，可以和主会的 jailbreak、unlearning、backdoor、privacy 论文互补。

