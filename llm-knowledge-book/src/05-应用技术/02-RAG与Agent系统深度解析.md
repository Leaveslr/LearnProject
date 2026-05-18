# RAG 与 Agent 系统深度解析

> 本章内容整理自 GitHub 高质量资源，涵盖 RAG 系统架构、Agent 编排、以及生产部署最佳实践

---

## 9.1 RAG vs Agent 对比

| 维度 | RAG系统 | Agent系统 |
|:---|:---|:---|
| **核心定位** | 检索增强生成，解决知识时效性和事实 grounding | 多步推理工作流编排，具备工具使用和规划能力 |
| **复杂度** | 中低（检索+生成） | 高（规划+执行+记忆） |
| **延迟** | 200-500ms | 1-5秒+ |
| **成本** | 中等 | 较高 |
| **可靠性** | 高（确定性检索管道） | 中等（多步骤可能失败） |
| **典型场景** | 知识问答、文档对话 | 任务自动化、复杂推理、工具调用 |

---

## 9.2 RAG 系统架构详解

### 三阶段流水线

```
检索 → 重排序 → 生成
```

### 检索与索引策略

| 组件 | 实现方案 | 权衡 |
|:---|:---|:---|
| 索引粒度 | 句子级/段落级/文档级 | 细粒度：精度高、存储大；粗粒度：上下文好、控制弱 |
| 向量表示 | BGE、Contriever、领域专用模型 | 语义覆盖 vs 领域特异性 |
| 混合搜索 | BM25 + 向量（加权组合） | 关键词精确 + 语义泛化 |
| ANN结构 | HNSW、FAISS、Milvus | 速度 vs 召回率 |
| 多路检索 | 并行多模型/多索引 | 更高召回、更大延迟 |

### 索引粒度选择

```
┌─────────────────────────────────────────────────────────────┐
│                    索引粒度对比                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  句子级 (256-512 tokens)                                     │
│  ✅ 精度高，相关性强                                        │
│  ❌ 丢失上下文，可能断章取义                                │
│  适用：事实问答、精确检索                                   │
│                                                              │
│  段落级 (512-1024 tokens)                                    │
│  ✅ 保留上下文，语义完整                                    │
│  ❌ 可能包含无关内容                                        │
│  适用：文档理解、复杂问答                                   │
│                                                              │
│  文档级 (1024-4096 tokens)                                   │
│  ✅ 完整上下文，全局理解                                    │
│  ❌ 精度下降，定位困难                                      │
│  适用：总结任务、主题检索                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 混合搜索实现

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.retrievers.bm25 import BM25Retriever

# 混合搜索：向量检索 + BM25
def create_hybrid_retriever(vector_store, bm25_store, weights=[0.6, 0.4]):
    vector_retriever = vector_store.as_retriever(
        similarity_top_k=10
    )
    bm25_retriever = BM25Retriever.from_defaults(
        index=bm25_store,
        similarity_top_k=10
    )
    
    return QueryFusionRetriever(
        retrievers=[vector_retriever, bm25_retriever],
        mode=QueryFusionRetriever.Mode.WEIGHTED_SUM,
        weights=weights
    )
```

### 向量数据库选择

| 数据库 | 特点 | 适用场景 |
|--------|------|----------|
| **FAISS** | Facebook 开源，CPU/GPU，高效 | 快速原型、小规模部署 |
| **Milvus** | 云原生，支持分布式 | 大规模生产环境 |
| **Qdrant** | Rust 实现，高性能 | 低延迟需求 |
| **Pinecone** | 全托管，MLOps 友好 | 快速上线，免运维 |
| **Weaviate** | 混合搜索，原生支持 | 混合检索需求 |

---

## 9.3 重排序器训练

### 负样本策略

正:负比例通常为 1:4 到 1:16

| 负样本类型 | 生成方式 | 效果 |
|-----------|----------|------|
| **随机负样本** | 随机采样无关文档 | 易采样，判别力提升有限 |
| **困难负样本** | 与正样本高相似但无关 | 判别力提升显著，但可能过难 |
| **半困难负样本** | 中等相似度，介于正负之间 | 难度适中，训练更稳定 |
| **批次内负样本** | 对比学习，共享前向传播 | 高效，适合大规模训练 |
| **动态挖掘** | 定期用当前模型重新挖掘 | 持续提升，适应分布变化 |

### Cross-Encoder 重排序

```python
from sentence_transformers import CrossEncoder

# 使用 Cross-Encoder 进行精排
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank_documents(query, documents, top_k=5):
    # 构建查询-文档对
    pairs = [(query, doc) for doc in documents]
    
    # 获取相关性分数
    scores = reranker.predict(pairs)
    
    # 按分数排序
    ranked_results = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )
    
    return [doc for doc, score in ranked_results[:top_k]]
```

### 重排序训练数据构建

```python
def build_reranker_training_data(queries, positives, hard_negatives):
    """
    构建交叉编码器训练数据
    
    Args:
        queries: 查询列表
        positives: 每个查询的正例文档
        hard_negatives: 每个查询的困难负例
    """
    training_data = []
    
    for query, pos_docs, neg_docs in zip(queries, positives, hard_negatives):
        # 1个正例 + N个负例
        for pos_doc in pos_docs:
            training_data.append({
                'query': query,
                'positive': pos_doc,
                'label': 1
            })
        for neg_doc in neg_docs:
            training_data.append({
                'query': query,
                'negative': neg_doc,
                'label': 0
            })
    
    return training_data
```

---

## 9.4 RAG 质量评估

### 三级评估框架

| 层级 | 指标 | 说明 |
|:---|:---|:---|
| **检索质量** | Recall@K, Precision@K, Hit@K, MRR, NDCG | 检索器是否找到相关文档 |
| **生成质量** | Faithfulness, Relevance, Fluency | LLM 生成内容的质量 |
| **端到端** | Answer Accuracy, Coverage, Latency, Cost | 整体系统效果 |

### 检索质量指标

```python
def evaluate_retrieval(retrieved_docs, relevant_docs, k_values=[1, 3, 5, 10]):
    """计算检索质量指标"""
    metrics = {}
    
    for k in k_values:
        # Recall@K: 相关文档在Top-K中的比例
        retrieved_k = set(retrieved_docs[:k])
        relevant = set(relevant_docs)
        recall = len(retrieved_k & relevant) / len(relevant) if relevant else 0
        
        # Precision@K: Top-K中相关文档的比例
        precision = len(retrieved_k & relevant) / k
        
        # Hit@K: Top-K中是否包含至少一个相关文档
        hit = 1 if retrieved_k & relevant else 0
        
        metrics[f'Recall@{k}'] = recall
        metrics[f'Precision@{k}'] = precision
        metrics[f'Hit@{k}'] = hit
    
    return metrics
```

### 生成质量评估

| 指标 | 定义 | 评估方法 |
|------|------|----------|
| **Faithfulness** | 生成内容是否忠实于检索文档 | LLM 判断或 NLI 模型 |
| **Relevance** | 生成内容是否与问题相关 | LLM 判断或 Embedding 相似度 |
| **Fluency** | 生成内容是否流畅通顺 | GPT 评分或语言模型困惑度 |
| **Context Utilization** | 是否充分利用了检索上下文 | 分析引用覆盖情况 |

---

## 9.5 Agent 系统架构

### 四大核心组件

```
用户理解 → 路由/规划 → 执行 → 记忆管理
```

### Agent 系统设计模式

```python
from abc import ABC, abstractmethod

class BaseAgent:
    """Agent 基类"""
    
    def __init__(self):
        self.tools = []
        self.memory = None
        self.planner = None
    
    def process(self, user_input: str) -> str:
        """Agent 主流程"""
        # 1. 理解用户意图
        intent = self.understand(user_input)
        
        # 2. 规划执行路径
        plan = self.planner.create_plan(intent)
        
        # 3. 执行工具调用
        results = self.execute(plan)
        
        # 4. 更新记忆
        self.memory.add_interaction(user_input, results)
        
        # 5. 生成最终响应
        return self.generate_response(results)
    
    @abstractmethod
    def understand(self, user_input: str) -> Intent:
        """理解用户意图"""
        pass
    
    @abstractmethod
    def execute(self, plan: Plan) -> List[ToolResult]:
        """执行工具调用"""
        pass
```

---

## 9.6 路由设计模式

### 两阶段路由策略

| 阶段 | 说明 | 示例 |
|:---|:---|:---|
| **硬约束过滤** | 上下文长度阈值、工具需求匹配、合规域验证 | 最多 ≤3 个候选模型 |
| **软评分排序** | 质量估计、成本权重、延迟权重、健康状态、历史成功率 | 加权综合评分 |

### 路由实现

```python
class Router:
    """智能路由"""
    
    def __init__(self, models_config):
        self.models = models_config
    
    def route(self, task: Task) -> Model:
        # 阶段1：硬约束过滤
        candidates = self._hard_filter(task)
        
        if len(candidates) == 0:
            return self.get_default_model()
        
        if len(candidates) == 1:
            return candidates[0]
        
        # 阶段2：软评分排序
        scored = []
        for model in candidates:
            score = self._compute_score(model, task)
            scored.append((model, score))
        
        # 选择最高分模型
        return max(scored, key=lambda x: x[1])[0]
    
    def _hard_filter(self, task: Task) -> List[Model]:
        """硬约束过滤"""
        candidates = []
        for model in self.models:
            if task.context_length <= model.max_context:
                if self._matches_domain(task, model):
                    candidates.append(model)
        return candidates[:3]  # 最多3个候选
    
    def _compute_score(self, model: Model, task: Task) -> float:
        """计算综合评分"""
        quality_score = model.quality_estimator.estimate(task)
        cost_weight = 0.3
        latency_weight = 0.2
        health_score = model.health_monitor.get_health()
        
        return (
            quality_score * 0.5 +
            (1 - model.normalized_cost) * cost_weight +
            (1 - model.normalized_latency) * latency_weight +
            health_score * 0.1
        )
```

### 熔断器机制

```python
class CircuitBreaker:
    """熔断器：防止级联故障"""
    
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half_open
    
    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half_open"
            else:
                raise CircuitOpenException("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            if self.state == "half_open":
                self.state = "closed"
                self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = "open"
            raise
```

---

## 9.7 深度搜索实现

### 迭代多跳研究工作流

```
规划 → 执行 → 反思 → 调整（循环）
```

### 实现示例

```python
class DeepSearchAgent:
    """深度搜索 Agent：多跳研究任务"""
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.max_iterations = 10
        self.budget = Budget(max_calls=20, max_time=120)
    
    def search(self, query: str) -> SearchResult:
        state = {
            'query': query,
            'findings': [],
            'visited_urls': set(),
            'iterations': 0
        }
        
        while self.budget.has_remaining() and state['iterations'] < self.max_iterations:
            # 1. 规划下一步
            plan = self._plan_next_step(state)
            
            if plan.action == "FINISH":
                break
            
            # 2. 执行
            result = self._execute_action(plan, state)
            
            # 3. 反思
            reflection = self._reflect(result, state)
            
            # 4. 更新状态
            if reflection.is_useful:
                state['findings'].append(result)
            state['iterations'] += 1
        
        # 5. 综合结论
        return self._synthesize(state['findings'])
    
    def _plan_next_step(self, state: dict) -> Plan:
        """使用 LLM 规划下一步"""
        prompt = f"""
        查询: {state['query']}
        已发现: {len(state['findings'])} 条信息
        已访问URL: {len(state['visited_urls'])} 个
        
        请规划下一步行动：
        - SEARCH: 执行网页搜索
        - VISIT: 访问特定URL获取详情
        - REFINE: 优化搜索查询
        - FINISH: 已有足够信息，生成答案
        """
        return self.llm.generate(prompt, output_format=Plan)
```

---

## 9.8 长期记忆管理

| 策略 | 实现 | 效果 |
|:---|:---|:---|
| 语义去重 | 存储前向量相似度检查（阈值过滤） | 防止语义重复存储 |
| 摘要压缩 | 分层摘要：局部→全局 | 减少存储，保留关键信息 |
| 记忆整合 | 定期合并相似事实为统一陈述 | 结构化知识 |
| 分层记忆 | 短期缓存 + 长期知识库 | 短期存近期上下文，长期存去重摘要 |
| 检索优化 | 多样性约束（MMR、聚类） | 避免检索语义相似结果 |

### 记忆管理实现

```python
class MemoryManager:
    """分层记忆管理"""
    
    def __init__(self, short_term_size=10, long_term_threshold=0.9):
        self.short_term = []  # 短期记忆：最近交互
        self.long_term = VectorStore()  # 长期记忆：语义存储
        self.short_term_size = short_term_size
        self.duplication_threshold = long_term_threshold
    
    def add(self, interaction: Interaction):
        """添加新交互"""
        # 检查是否需要去重
        if self._is_duplicate(interaction):
            return
        
        # 添加到短期记忆
        self.short_term.append(interaction)
        
        # 超过容量时压缩到长期记忆
        if len(self.short_term) > self.short_term_size:
            self._compress_to_long_term()
    
    def retrieve(self, query: str, k: int = 5) -> List[Memory]:
        """检索记忆"""
        results = []
        
        # 短期记忆优先（近因效应）
        results.extend(self.short_term[-k:])
        
        # 长期记忆语义检索
        long_term_results = self.long_term.search(query, k=k)
        results.extend(long_term_results)
        
        return results
    
    def _is_duplicate(self, interaction: Interaction) -> bool:
        """语义去重检查"""
        if not self.short_term:
            return False
        
        embedding = self.embed(interaction.content)
        recent_embeddings = self.embed([m.content for m in self.short_term[-5:]])
        
        similarity = cosine_similarity([embedding], recent_embeddings)[0]
        return max(similarity) > self.duplication_threshold
    
    def _compress_to_long_term(self):
        """压缩短期记忆到长期记忆"""
        # 生成摘要
        summary = self._summarize(self.short_term)
        
        # 存储到向量数据库
        self.long_term.add(summary)
        
        # 清空短期记忆
        self.short_term = []
```

---

## 9.9 生产部署最佳实践

### 故障模式与缓解策略

| 故障模式 | 系统 | 缓解策略 |
|:---|:---|:---|
| 检索召回差 | RAG | 多路检索、查询扩展、嵌入微调 |
| 有证据仍幻觉 | RAG | 重排序器质量提升、提示工程、忠实性惩罚 |
| 工具选择错误 | Agent | 路由A/B测试、回退规则、用户反馈闭环 |
| 记忆溢出 | Agent | 积极摘要、滑动窗口、基于相关性的淘汰 |
| 级联故障 | Agent | 每工具熔断器、超时预算、优雅降级 |
| 高延迟 | 两者 | 缓存、并行执行、模型蒸馏、批处理 |

### Agent 延迟优化

| 策略 | 说明 |
|:---|:---|
| 串行→并行 | 独立工具调用转为并行 DAG 执行 |
| 工具路由 | 小模型或规则仅调用必要工具 |
| 高频缓存 | 缓存查询结果、文档、嵌入 |
| 推理加速 | KV-Cache、动态批处理、流式输出 |
| 提示压缩 | 最小化系统提示和历史上下文 |
| 可观测性 | 全链路追踪，关注 p95/p99 延迟 |

### RAG + Agent 集成架构

```python
class RAGAgent:
    """RAG 与 Agent 集成"""
    
    def __init__(self, llm, rag_system, tools):
        self.llm = llm
        self.rag = rag_system
        self.tools = tools
    
    def process(self, query: str) -> str:
        # Agent 决策：是否需要 RAG
        plan = self.llm.plan(query)
        
        results = []
        
        for step in plan.steps:
            if step.requires_rag:
                # 调用 RAG 系统
                rag_result = self.rag.query(step.sub_query)
                results.append(('rag', rag_result))
            
            for tool_name in step.tools:
                # 调用其他工具
                tool_result = self.tools[tool_name].execute(step.params)
                results.append((tool_name, tool_result))
            
            # Agent 反思：根据结果调整下一步
            if step.needs_reflection:
                reflection = self.llm.reflect(results[-1])
                if not reflection.is_satisfied:
                    # 调整计划重试
                    pass
        
        # 综合所有结果生成最终答案
        return self.llm.synthesize(query, results)
```

---

## 9.10 面试高频问题

### Q1: RAG vs 微调怎么选？

> **RAG 优势**：知识可更新、无需重新训练、解释性强、适合知识密集型任务
> **微调优势**：行为更一致、延迟更低、适合风格/格式控制
> **选择原则**：
> - 知识时效性强 → RAG
> - 需要特定格式/风格 → 微调
> - 两者结合效果最好

### Q2: 如何提升 RAG 召回率？

> 1. **多路检索**：向量 + BM25 + 关键词组合
> 2. **查询扩展**：用 LLM 改写/扩展查询
> 3. **嵌入微调**：针对领域数据微调 Embedding 模型
> 4. **重排序**：先用向量召回 Top-K，再用 Cross-Encoder 精排
> 5. **迭代检索**：多跳查询逐步深入

### Q3: Agent 系统如何保证可靠性？

> 1. **熔断器机制**：单工具失败不影响整体
> 2. **超时预算**：限制总执行时间，防止无限循环
> 3. **回退策略**：Agent 失败时降级到简单方案
> 4. **结果验证**：LLM 或规则验证工具输出
> 5. **可观测性**：全链路追踪，快速定位问题

### Q4: 多模态 Agent 怎么设计？

> **感知器-推理器架构**：
> 1. 感知器：粗粒度全局理解，生成结构化摘要
> 2. 推理器：分析缺口，生成目标查询
> 3. 感知器执行：ROI 特定任务，局部证据
> 4. 证据融合：冲突解决，聚合结论
> 5. 终止判断：关键缺口填满或预算耗尽

### Q5: 长期记忆怎么处理？

> 1. **分层存储**：短期（最近交互）+ 长期（语义向量）
> 2. **语义去重**：相似内容不重复存储
> 3. **摘要压缩**：定期将短期记忆压缩为摘要
> 4. **相关性检索**：按当前任务相关性获取记忆
> 5. **容量管理**：LRU 或基于重要性的淘汰策略

---

## 参考文献

- [yuyouyu32/llm-interview](https://github.com/yuyouyu32/llm-interview) - LLM应用模式与Agent系统
- [Lau-Jonathan/LLM-Agent-Interview-Guide](https://github.com/Lau-Jonathan/LLM-Agent-Interview-Guide) - Agent面试指南
- [RAG Survey Papers](https://arxiv.org/abs/2312.10997) - RAG 综述论文
