# 第六章：RAG 系统架构

## 6.1 RAG 概述

### 6.1.1 什么是 RAG？

RAG（Retrieval-Augmented Generation，检索增强生成）是一种结合**检索系统**和**生成模型**的技术，让 LLM 能够利用外部知识库回答问题。

```
┌──────────────────────────────────────────────────────────────┐
│                        RAG 流程                               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   用户问题 ──► 查询检索 ──► 向量数据库 ──► 获取相关文档       │
│                    ↓                                         │
│              构造 Prompt ──► LLM 生成答案                    │
│                    ↓                                         │
│              最终回答                                         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 6.1.2 为什么需要 RAG？

| 方案 | 优势 | 劣势 |
|------|------|------|
| **纯 LLM** | 生成流畅 | 知识可能过时/幻觉 |
| **RAG** | 利用最新知识、减少幻觉、可溯源 | 增加系统复杂度 |
| **微调** | 适应特定领域 | 成本高、知识更新慢 |

---

## 6.2 RAG 核心组件

### 6.2.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                        RAG 系统                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 数据摄入 (Ingestion)                                    │
│  ┌─────────┐    ┌──────────┐    ┌─────────────────┐       │
│  │ 文档    │───►│ 文档解析  │───►│ 文本分块        │       │
│  └─────────┘    └──────────┘    └────────┬────────┘       │
│                                          │                 │
│                                          ▼                 │
│  ┌──────────┐    ┌──────────┐    ┌─────────────┐         │
│  │ Embedding│◄───│ 嵌入模型  │◄───│ 块列表     │         │
│  └──────────┘    └──────────┘    └──────┬──────┘         │
│                                          │                 │
│                                          ▼                 │
│                                  ┌───────────────┐         │
│                                  │ 向量数据库     │         │
│                                  └───────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  2. 检索推理 (Retrieval)                                    │
│  ┌─────────┐    ┌──────────┐    ┌─────────────────┐       │
│  │ 用户查询 │───►│ 查询编码  │───►│ 向量相似度搜索  │       │
│  └─────────┘    └──────────┘    └────────┬────────┘       │
│                                           │                 │
│                                           ▼                 │
│                                  ┌───────────────┐         │
│                                  │ Top-K 相关文档 │         │
│                                  └───────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  3. 生成 (Generation)                                        │
│  ┌────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ 原始问题   │ +  │ 检索文档    │ ─► │ 构造 Prompt │     │
│  └────────────┘    └─────────────┘    └──────┬──────┘     │
│                                              │              │
│                                              ▼              │
│                                      ┌─────────────┐       │
│                                      │  LLM 生成   │       │
│                                      └─────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2.2 组件详解

| 组件 | 功能 | 常见工具 |
|------|------|---------|
| **文档解析** | 提取文本、表格、图片 | Unstructured、Pdfminer |
| **文本分块** | 将长文档分割成小块 | LangChain、LlamaIndex |
| **嵌入模型** | 将文本转为向量 | OpenAI-ada2、BGE、M3E |
| **向量数据库** | 存储和检索向量 | Milvus、Pinecone、Chroma |
| **生成模型** | 根据上下文生成答案 | GPT-4、Qwen、LLaMA |

---

## 6.3 文档解析与预处理

### 6.3.1 支持的文档格式

- PDF（最常见）
- Word (.docx)
- Excel (.xlsx)
- PowerPoint (.pptx)
- Markdown
- HTML
- 图片（需要 OCR）

### 6.3.2 文档解析代码示例

```python
from unstructured.partition.pdf import partition_pdf
from typing import List

def parse_pdf(file_path: str) -> List[str]:
    """解析 PDF 文件，提取文本内容"""
    elements = partition_pdf(
        filename=file_path,
        strategy="hi_res",  # 高分辨率策略
        extract_images_table_metadata=True,
    )
    
    # 过滤并拼接文本
    texts = []
    for element in elements:
        if hasattr(element, 'text'):
            texts.append(element.text)
    
    return texts
```

---

## 6.4 文本分块策略

### 6.4.1 分块策略对比

| 策略 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **固定大小** | 简单快速 | 可能切断句子 | 日志、代码 |
| **句子级** | 语义完整 | 块大小不均 | 通用文本 |
| **递归字符** | 保留自然边界 | 需要调参 | LangChain 默认 |
| **语义分块** | 主题一致 | 计算量大 | 主题多样的文档 |
| **文档结构** | 保留层次 | 依赖格式 | Markdown、PDF |

### 6.4.2 固定大小分块

```python
def fixed_size_chunk(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """固定大小分块，带重叠"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # 重叠移动
    return chunks
```

### 6.4.3 语义分块

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def semantic_chunk(texts: List[str], threshold: float = 0.5) -> List[str]:
    """基于句子相似度的语义分块"""
    if len(texts) <= 1:
        return [" ".join(texts)]
    
    # 计算相邻句子的相似度
    embeddings = embed_model.encode(texts)
    similarities = cosine_similarity(embeddings[:-1], embeddings[1:])
    
    # 根据相似度阈值切分
    chunks = []
    current_chunk = [texts[0]]
    
    for i, sim in enumerate(similarities):
        if sim < threshold:
            chunks.append(" ".join(current_chunk))
            current_chunk = [texts[i + 1]]
        else:
            current_chunk.append(texts[i + 1])
    
    chunks.append(" ".join(current_chunk))
    return chunks
```

---

## 6.5 检索技术

### 6.5.1 检索类型

```
┌─────────────────────────────────────────────────────────────┐
│                        检索类型                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 稀疏检索 (Sparse Retrieval)                            │
│     - 基于词频/BM25                                        │
│     - 擅长精确关键词匹配                                     │
│                                                             │
│  2. 密集检索 (Dense Retrieval)                             │
│     - 基于向量相似度                                         │
│     - 擅长语义理解                                          │
│                                                             │
│  3. 混合检索 (Hybrid Retrieval)                           │
│     - 稀疏 + 密集                                          │
│     - 互补优势                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.5.2 BM25 算法

BM25 是基于词频的经典检索算法：

```
Score(D, Q) = Σ IDF(q_i) * (f(q_i, D) * (k1 + 1)) / 
              (f(q_i, D) + k1 * (1 - b + b * |D|/avgdl))
```

- f(q_i, D): 词项 q_i 在文档 D 中的频率
- |D|: 文档长度
- avgdl: 平均文档长度
- k1, b: 超参数

### 6.5.3 向量检索

```python
# 使用 Milvus 进行向量检索
from pymilvus import MilvusClient

client = MilvusClient("milvus_demo.db")
collection = client.get_collection("documents")

# 检索
query_embedding = embed_model.encode(["用户问题"])
results = collection.search(
    data=[query_embedding[0].tolist()],
    anns_field="embedding",
    param={"metric_type": "IP", "params": {"nprobe": 10}},
    limit=5,  # Top-K
    output_fields=["text", "source"]
)
```

---

## 6.6 混合检索与重排序

### 6.6.1 Reciprocal Rank Fusion (RRF)

融合多路检索结果：

```python
def reciprocal_rank_fusion(results_list: List[List[dict]], k: int = 60) -> List[dict]:
    """RRF 算法融合多路检索结果"""
    scores = {}
    
    for results in results_list:
        for rank, doc in enumerate(results):
            doc_id = doc["id"]
            # RRF 公式: 1 / (k + rank)
            score = 1 / (k + rank + 1)
            scores[doc_id] = scores.get(doc_id, 0) + score
    
    # 按得分排序
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [doc_id for doc_id, _ in ranked]
```

### 6.6.2 重排序（Re-ranking）

```python
from sentence_transformers import CrossEncoder

# 使用 Cross-Encoder 重排序
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query: str, documents: List[str], top_k: int = 10) -> List[dict]:
    """使用 Cross-Encoder 重排序"""
    pairs = [(query, doc) for doc in documents]
    scores = cross_encoder.predict(pairs)
    
    ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    return [{"text": doc, "score": score} for doc, score in ranked[:top_k]]
```

---

## 6.7 面试高频问题

### Q1: RAG 有哪些优化手段？

> 1. **索引阶段**：更好的分块策略、元数据过滤、层次索引
> 2. **检索阶段**：混合检索、重排序、查询扩展/改写
> 3. **生成阶段**：上下文压缩、引用标注、Prompt 优化

### Q2: 如何选择分块大小？

> 取决于任务特点：短块（200-300 tokens）适合精确匹配；长块（500-1000 tokens）适合需要上下文的场景。通常需要实验调优。

### Q3: 什么是多跳检索？

> 多跳检索指需要跨多个文档进行推理的问题（如"XX公司的CEO和竞争对手的CTO是什么关系？"）。需要迭代检索和推理。

### Q4: RAG vs Fine-tuning 怎么选？

> RAG 适合：知识频繁更新、需要可解释性、数据有限
> Fine-tuning 适合：领域特定语言/风格、任务固定、已有大量标注数据

---

*参考文献*
- Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", 2020
- https://github.com/aceliuchanghong/FAQ_Of_LLM_Interview
