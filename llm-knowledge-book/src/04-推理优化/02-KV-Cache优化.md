# 第十一章：推理优化技术

## 11.1 推理优化的重要性

### 11.1.1 为什么需要优化？

```
┌─────────────────────────────────────────────────────────────┐
│                    推理 vs 训练                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  训练:                                                       │
│  - 批量处理大批量数据                                        │
│  - 可以长时间运行                                            │
│  - 关注模型质量                                              │
│                                                              │
│  推理:                                                       │
│  - 低延迟要求（毫秒级响应）                                  │
│  - 高并发（同时服务大量用户）                                 │
│  - 成本敏感（每次调用都要算钱）                              │
│  - 资源有限（GPU 显存、带宽）                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 11.2 KV Cache

### 11.2.1 什么是 KV Cache？

在自回归生成中，每个新 token 都需要 attend 到之前的所有 token，导致重复计算。KV Cache 通过缓存之前的 K 和 V 来避免这种重复。

```python
# 没有 KV Cache
for new_token in generated_tokens:
    # 每次都重新计算所有 token 的 K, V
    k, v = compute_kv(all_tokens)
    output = attention(q, k, v)

# 有 KV Cache
k_cache, v_cache = [], []
for new_token in generated_tokens:
    k_new, v_new = compute_kv(new_token)
    k_cache.append(k_new)
    v_cache.append(v_new)
    output = attention(q, k_cache, v_cache)  # 只计算新 token 的 K, V
```

### 11.2.2 KV Cache 的问题

| 问题 | 说明 |
|------|------|
| **显存占用** | 长度越长，缓存越大（O(n)） |
| **内存碎片** | 不连续分配导致浪费 |
| **管理复杂** | 需要跟踪每个请求的缓存 |

### 11.2.3 PagedAttention

vLLM 提出的方案，模仿操作系统的虚拟内存分页：

```python
# 传统 KV Cache
每个请求占用连续显存
[Token 1][Token 2][Token 3][...全部预分配]

# PagedAttention
将 KV Cache 分割成固定大小的块
[Block 1][Block 2][Block 3]  ← 动态分配，不需预分配
```

---

## 11.3 量化技术

### 11.3.1 量化概述

```
┌─────────────────────────────────────────────────────────────┐
│                      量化精度对比                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  FP32 (32-bit Float):  精度最高，显存最大                    │
│  ┌────┐                                                     │
│  │████│ = 4 bytes                                          │
│  └────┘                                                     │
│                                                              │
│  FP16/BF16 (16-bit):  平衡方案，H100/H800 优化             │
│  ┌──┐                                                        │
│  │██│ = 2 bytes                                             │
│  └──┘                                                        │
│                                                              │
│  INT8 (8-bit Int):     量化方法，精度损失较小                │
│  ┌─┐                                                          │
│  │▌│ = 1 byte                                               │
│  └─┘                                                          │
│                                                              │
│  INT4 (4-bit):        极致压缩，需特殊处理                   │
│  ┌┐                                                            │
│  ││ = 0.5 bytes                                             │
│  └┘                                                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 11.3.2 量化方法对比

| 方法 | 精度 | 显存减少 | 速度 | 适用场景 |
|------|------|---------|------|---------|
| **FP16** | 基准 | 1x | 基准 | 通用 |
| **INT8** | ~99% | 2x | 1.5-2x | 均衡场景 |
| **AWQ** | ~98% | 4x | 2-3x | 低延迟 |
| **GPTQ** | ~97% | 4x | 2-3x | 批量推理 |
| **GGUF** | ~95% | 4x | 依赖硬件 | CPU/本地 |

### 11.3.3 AWQ 量化代码

```python
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

# 加载模型
model_path = "meta-llama/Llama-3-8B-Instruct"
model = AutoAWQForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# 量化配置
quant_config = {
    "zero_point": True,
    "q_group_size": 128,
    "w_bit": 4,
    "version": "GEMM"
}

# 量化
model.quantize(tokenizer, quant_config=quant_config)

# 保存
quant_path = "./llama3-8b-awq"
model.save_quantized(quant_path)
tokenizer.save_pretrained(quant_path)
```

---

## 11.4 推理框架

### 11.4.1 主流框架对比

| 框架 | 特点 | 适用场景 |
|------|------|---------|
| **vLLM** | PagedAttention、Continuous Batching | 高并发服务 |
| **SGLang** | RadixAttention、前缀缓存 | 复杂推理任务 |
| **LMDeploy** | TurboMind、自研算子 | 国产 GPU |
| **TensorRT-LLM** | TensorRT 优化 | 极致性能 |

### 11.4.2 vLLM 部署代码

```python
# 使用 vLLM 启动服务
# 命令行
# vllm serve Qwen/Qwen2.5-72B-Instruct \
#     --quantization awq \
#     --tensor-parallel-size 8 \
#     --gpu-memory-utilization 0.95

# API 调用
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"
)

response = client.chat.completions.create(
    model="Qwen2.5-72B-Instruct",
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手"},
        {"role": "user", "content": "解释一下什么是大模型"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### 11.4.3 SGLang 前缀缓存

```python
# SGLang 支持自动识别和缓存共享前缀
# System prompt 和工具定义通常不变，可以复用

response = client.chat.completions.create(
    model="Qwen2.5-72B-Instruct",
    messages=[
        {"role": "system", "content": "你是一个专业的AI助手..."},  # 可缓存
        {"role": "user", "content": "今天天气如何？"}               # 变化部分
    ],
    extra_body={
        "enable_prefix_caching": True  # 启用前缀缓存
    }
)
```

---

## 11.5 并行策略

### 11.5.1 Tensor Parallelism

将模型参数按维度分割到多个 GPU：

```python
# vLLM 多卡部署
# 8 卡运行 72B 模型
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-72B-Instruct \
    --tensor-parallel-size 8 \
    --gpu-memory-utilization 0.9
```

### 11.5.2 Continuous Batching

动态批处理，多个请求共享 GPU 资源：

```
┌─────────────────────────────────────────────────────────────┐
│                    Continuous Batching                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  请求 A: [Tokens 1-5] ──────► [完成]                        │
│  请求 B: [Tokens 1-3] ───► [等待] ───► [继续] ──► [完成]  │
│  请求 C: ───► [Tokens 1-7] ──────► [完成]                  │
│                                                              │
│  GPU: ████████████████████████████████████████              │
│                                                              │
│  动态添加新请求，最大化 GPU 利用率                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 11.6 面试高频问题

### Q1: 什么是 KV Cache？

> 在自回归生成中，KV Cache 缓存之前 token 的 Key 和 Value 向量，避免重复计算。新 token 只需 attend 到缓存的 K/V 和当前 token 的 K/V。

### Q2: PagedAttention 是什么？

> vLLM 提出的技术，将 KV Cache 分割成固定大小的块，动态分配显存，避免预分配导致的碎片化和浪费。

### Q3: 量化会损失多少精度？

> INT8 通常损失 <1%，INT4 损失 2-5%。AWQ/GPTQ 等方法通过校准可以进一步减少精度损失。

### Q4: 如何选择量化方法？

> INT8：均衡场景，精度损失小
> AWQ：低延迟推理，CPU 部署
> GPTQ：批量推理服务端
> GGUF：本地/边缘部署

### Q5: 推理框架怎么选？

> vLLM：高并发在线服务首选
> SGLang：复杂推理任务、多轮对话
> TensorRT-LLM：极致性能要求
> LMDeploy：国产 GPU 或特殊需求

---

*参考文献*
- Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention", 2023
- https://github.com/aceliuchanghong/FAQ_Of_LLM_Interview
