# AI 大模型面试宝典

> 一本全面覆盖大模型算法岗面试的核心指南

**适用人群**：算法工程师 / 大模型算法岗 / AI Engineer

**涵盖范围**：Transformer · Attention · 位置编码 · MoE · LoRA · RLHF · RAG · Agent · 推理优化 · 分布式训练

---

## 当前进度

✅ **已创建 17 个核心章节 + 13 个真实面试题文件**

---

### 🆕 新增内容 (2026-04-13)

#### 主流模型架构 (新增)
- [第三十九章：主流模型架构深度对比](./src/07-主流模型架构/01-主流模型架构深度对比.md) - DeepSeek V3/Llama 4/Qwen3/Gemma 3/MoE架构/MLA vs GQA
- [第四十章：多模态大模型架构与面试](./src/07-主流模型架构/02-多模态大模型架构与面试.md) - GPT-4V/LLaVA/Qwen-VL/视觉编码器/模态对齐

#### AI Agent 进阶 (新增)
- [第三十一章：Agent进阶：多模态Agent与生产实战](./src/06-Agent/02-Agent进阶：多模态Agent与生产实战.md) - Multi-Agent/RAG架构/LangChain/LangGraph
- [第三十二章：多智能体协作与面试实战](./src/06-Agent/03-多智能体协作与面试实战.md) - Multi-Agent协作/ReAct/任务分解

---

## 目录

### 第一部分：基础原理
- [第一章：机器学习基础](./src/01-基础原理/01-机器学习基础.md)
- [第二章：深度学习基础](./src/01-基础原理/02-深度学习基础.md)

### 第二部分：模型架构
- [第三章：Transformer 架构详解](./src/02-模型架构/01-Transformer详解.md)
- [第四章：注意力机制深度剖析](./src/02-模型架构/02-注意力机制.md)
- [第五章：位置编码](./src/02-模型架构/03-位置编码.md)
- [第六章：多头注意力与变体（MHA/MQA/GQA/MLA）](./src/02-模型架构/04-多头注意力变体.md)
- [第七章：FFN 与激活函数](./src/02-模型架构/05-FFN与激活函数.md)
- [第八章：混合专家模型 MoE](./src/02-模型架构/06-MoE详解.md)

### 第三部分：训练技术
- [第九章：预训练与自监督学习](./src/03-训练技术/01-预训练.md)
- [第十章：SFT 有监督微调](./src/03-训练技术/02-SFT微调.md)
- [第十一章：RLHF 与对齐技术](./src/03-训练技术/03-RLHF对齐.md)
- [第十二章：DPO 详解](./src/03-训练技术/04-DPO详解.md)
- [第十三章：GRPO 与 GSPO](./src/03-训练技术/05-GRPO-GSPO.md)
- [第十四章：PEFT 高效微调](./src/03-训练技术/06-PEFT高效微调.md)
- [第十五章：LoRA 原理与实战](./src/03-训练技术/07-LoRA详解.md)
- [第十六章：分布式训练](./src/03-训练技术/08-分布式训练.md)

### 第四部分：推理优化
- [第十七章：推理框架（vLLM/SGLang/LMDeploy）](./src/04-推理优化/01-推理框架.md)
- [第十八章：KV Cache 优化](./src/04-推理优化/02-KV-Cache优化.md)
- [第十九章：量化技术（AWQ/GPTQ/GGUF）](./src/04-推理优化/03-量化技术.md)
- [第二十章：模型部署实战](./src/04-推理优化/04-模型部署.md)

### 第五部分：应用技术
- [第二十一章：RAG 系统架构](./src/05-应用技术/01-RAG系统架构.md)
- [第二十二章：RAG 优化策略](./src/05-应用技术/02-RAG优化.md)
- [第二十三章：Embedding 与向量数据库](./src/05-应用技术/03-Embedding向量库.md)
- [第二十四章：Prompt Engineering](./src/05-应用技术/04-Prompt工程.md)

### 第六部分：AI Agent
- [第二十五章：AI Agent 基础概念](./src/06-Agent/01-Agent基础.md)
- [第二十六章：Agent 开发范式](./src/06-Agent/02-Agent开发范式.md)
- [第二十七章：LangGraph 实战](./src/06-Agent/03-LangGraph实战.md)
- [第二十八章：Agent 记忆系统](./src/06-Agent/04-Agent记忆系统.md)
- [第二十九章：MCP 协议](./src/06-Agent/05-MCP协议.md)
- [第三十章：Human-in-the-Loop](./src/06-Agent/06-Human-in-the-Loop.md)

### 第七部分：主流模型
- [第三十一章：GPT 系列演进](./src/07-主流模型/01-GPT系列.md)
- [第三十二章：LLaMA 系列](./src/07-主流模型/02-LLaMA系列.md)
- [第三十三章：DeepSeek 系列](./src/07-主流模型/03-DeepSeek系列.md)
- [第三十四章：Qwen 系列](./src/07-主流模型/04-Qwen系列.md)

### 第八部分：面试技巧
- [第三十五章：面试必问问题](./src/08-面试技巧/01-必问问题.md)
- [第三十六章：自我介绍模板](./src/08-面试技巧/02-自我介绍.md)
- [第三十七章：谈薪技巧](./src/08-面试技巧/03-谈薪技巧.md)
- [第三十八章：HR 常问问题](./src/08-面试技巧/04-HR问题.md)

---

## 资料来源

本书内容整理自以下优质开源资源：

1. **FAQ_Of_LLM_Interview** - 大模型算法岗面试题库 (1.8k stars)
   - GitHub: https://github.com/aceliuchanghong/FAQ_Of_LLM_Interview

2. **LLMs Interview Questions** - DevInterview.io (63道面试题)
   - GitHub: https://github.com/Devinterview-io/llms-interview-questions

3. **AI Engineering Interview Questions** - AI工程面试题
   - GitHub: https://github.com/amitshekhariitbhu/ai-engineering-interview-questions

4. **LLM Interview Guide** - yuyouyu32 深度面试指南
   - GitHub: https://github.com/yuyouyu32/llm-interview
   - 涵盖：训练方法、部署优化、应用模式等深度内容

5. **LLM Agent Interview Guide** - 量化与Agent面试指南
   - GitHub: https://github.com/Lau-Jonathan/LLM-Agent-Interview-Guide
   - 涵盖：模型量化、部署架构、Agent系统

6. **Awesome-LLM-Interview-Questions** - 精选面试题集合
   - GitHub: https://github.com/sreekanth-madisetty/Awesome-LLM-Interview-Questions

7. **AgentGuide** - AI Agent 开发学习指南
   - https://adongwanai.github.io/AgentGuide/
   - 涵盖：LangChain/LangGraph 实战、高级 RAG、大模型面试

8. **MLLM Survey** - 多模态大语言模型综述
   - arxiv: 2306.13549
   - 涵盖：视觉编码器、模态对齐、训练策略

9. **Awesome-Multimodal-RAG** - 多模态 RAG 资源集合
   - GitHub: https://github.com/JarvisUSTC/Awesome-Multimodal-RAG
   - 涵盖：多模态检索增强生成最新进展

10. **Sebastian Raschka LLM 架构对比** - 2025年主流模型深度分析
    - https://magazine.sebastianraschka.com
    - 涵盖：DeepSeek V3/Llama 4/Gemma 3 架构创新

11. **Modern LLM Architecture Comparison** - 可视化架构对比
    - https://profitmonk.github.io/visual-ai-tutorials/architecture-comparison.html
    - 涵盖：MLA/GQA/滑动窗口注意力深度对比

---

*最后更新：2026年4月*
