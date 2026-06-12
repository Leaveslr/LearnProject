# Agent 进阶：多模态 Agent 与生产实战

> 本章深入讲解多模态 Agent 系统设计、生产级 RAG 架构、Agent 评估方法，以及主流 Agent 框架（LangChain/LangGraph）实战技巧。

---

## 目录

1. [多模态 Agent 系统架构](#一多模态-agent-系统架构)
2. [生产级 RAG 架构设计](#二生产级-rag-架构设计)
3. [Agent 评估方法](#三agent-评估方法)
4. [LangChain/LangGraph 实战](#四langchainlanggraph-实战)
5. [Agent 生产最佳实践](#五agent-生产最佳实践)
6. [面试高频问题](#六面试高频问题)

---

## 一、多模态 Agent 系统架构

### 1.1 多模态 Agent 定义

```
多模态 Agent = LLM (大脑) + 工具调用 (四肢) + 多模态感知 (五官)

核心能力:
- 视觉理解: 图像、视频、文档
- 工具调用: API、代码执行、搜索
- 任务规划: 复杂任务分解
- 自我反思: 错误检测与修正
```

### 1.2 ReAct 范式深化

```python
# 多模态 ReAct 实现
class MultimodalReActAgent:
    def __init__(self, llm, tools, vision_encoder=None):
        self.llm = llm
        self.tools = tools
        self.vision_encoder = vision_encoder
    
    def think(self, state):
        """思考下一步行动"""
        context = self._build_context(state)
        
        prompt = f"""
        当前任务: {state.task}
        已完成步骤: {state.history}
        
        可用工具:
        {self._format_tools()}
        
        思考: (Thought)
        """
        
        response = self.llm.chat(prompt)
        return self._parse_response(response)
    
    def act(self, thought):
        """执行行动"""
        if thought.type == 'tool':
            return self._execute_tool(thought.tool, thought.params)
        elif thought.type == 'vision':
            return self._process_image(thought.image)
        else:
            return self.llm.generate(thought.text)
    
    def observe(self, result):
        """观察结果并决定下一步"""
        return f"观察结果: {result}\n下一步行动是什么?"
```

### 1.3 多模态工具调用

```python
# 多模态工具定义
class MultimodalTool:
    def __init__(self, name, description, input_schema, vision_required=False):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.vision_required = vision_required

# 示例工具
tools = [
    MultimodalTool(
        name="analyze_chart",
        description="分析图表图像，提取数据信息",
        input_schema={
            "image_url": "str",  # 图表图片URL
            "question": "str"     # 具体分析问题
        },
        vision_required=True
    ),
    MultimodalTool(
        name="search_documents",
        description="搜索企业内部文档",
        input_schema={
            "query": "str",
            "doc_type": "str"  # pdf, markdown, slides
        },
        vision_required=False
    ),
    MultimodalTool(
        name="generate_image",
        description="根据描述生成图像",
        input_schema={
            "prompt": "str",
            "style": "str"  # realistic, cartoon, diagram
        },
        vision_required=False
    )
]
```

### 1.4 多模态 Agent 架构图

```
┌─────────────────────────────────────────────────────────┐
│                    多模态 Agent 系统                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│  │ 图像输入  │    │ 视频输入  │    │ 文档输入  │         │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘         │
│       │              │              │                   │
│       └──────────────┼──────────────┘                 │
│                      ▼                                  │
│            ┌─────────────────┐                         │
│            │  多模态感知层    │                         │
│            │ Vision Encoder  │                         │
│            └────────┬────────┘                         │
│                     │                                   │
│                     ▼                                   │
│            ┌─────────────────┐                         │
│            │  任务规划层      │                         │
│            │  (Planner)       │                         │
│            └────────┬────────┘                         │
│                     │                                   │
│       ┌─────────────┼─────────────┐                    │
│       ▼             ▼             ▼                     │
│  ┌────────┐   ┌────────┐   ┌────────┐                  │
│  │ 工具1  │   │ 工具2  │   │ 工具3  │                  │
│  │分析图表│   │搜索文档│   │生成图像│                  │
│  └────────┘   └────────┘   └────────┘                  │
│                     │                                   │
│                     ▼                                   │
│            ┌─────────────────┐                         │
│            │  结果整合层      │                         │
│            │  Response Gen   │                         │
│            └─────────────────┘                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 二、生产级 RAG 架构设计

### 2.1 企业级 RAG 架构

```
┌──────────────────────────────────────────────────────────────┐
│                     企业级 RAG 系统                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  数据源层                                                     │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐    │
│  │ Notion │ │ Conflu │ │ Slack  │ │ Email  │ │ 数据库  │    │
│  └────┬───┘ └────┬───┘ └────┬───┘ └────┬───┘ └───┬────┘    │
│       │          │          │          │          │          │
│  ┌────┴──────────┴──────────┴──────────┴──────────┴────┐   │
│  │              Connector / 爬虫 / API 接入              │   │
│  └────────────────────────┬─────────────────────────────┘   │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │                   文档处理管道                        │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │     │
│  │  │ 内容提取 │→ │ 分块策略 │→ │ 元数据增强 │          │     │
│  │  │(PDF/HTML)│  │(语义/层次)│  │ (来源/时间)│          │     │
│  │  └──────────┘  └──────────┘  └──────────┘          │     │
│  └────────────────────────┬─────────────────────────────┘     │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │               向量数据库 / 知识库                    │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │ Chroma │ Milvus │ Pinecone │ Qdrant │ ... │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  └────────────────────────┬─────────────────────────────┘     │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │                  查询处理管道                        │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │     │
│  │  │ 查询改写 │→ │ 意图识别 │→ │ 查询扩展 │          │     │
│  │  └──────────┘  └──────────┘  └──────────┘          │     │
│  └────────────────────────┬─────────────────────────────┘     │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │                    检索引擎                          │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │     │
│  │  │ 向量检索 │→ │ 混合检索 │→ │ Reranker │          │     │
│  │  └──────────┘  └──────────┘  └──────────┘          │     │
│  └────────────────────────┬─────────────────────────────┘     │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │                  生成层 (LLM)                        │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │        Context + Query → Answer          │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 高级检索策略

#### 2.2.1 混合检索 (Hybrid Search)

```python
class HybridRetriever:
    """混合检索: 向量 + 关键词"""
    
    def retrieve(self, query, top_k=10, alpha=0.5):
        """
        alpha: 0=纯关键词, 1=纯向量
        """
        # 向量检索
        vector_results = self.vector_index.search(
            query, k=top_k * 2
        )
        
        # BM25 关键词检索
        bm25_results = self.bm25_index.search(
            query, k=top_k * 2
        )
        
        # Reciprocal Rank Fusion (RRF)
        fused_scores = {}
        for rank, doc in enumerate(vector_results):
            fused_scores[doc.id] = fused_scores.get(doc.id, 0) + \
                1 / (60 + rank)
        
        for rank, doc in enumerate(bm25_results):
            fused_scores[doc.id] = fused_scores.get(doc.id, 0) + \
                1 / (60 + rank)
        
        # 排序取 top_k
        sorted_docs = sorted(
            fused_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:top_k]
        
        return [self.doc_store.get(id) for id, _ in sorted_docs]
```

#### 2.2.2 查询改写与扩展

```python
class QueryRewriter:
    """查询改写提升检索质量"""
    
    def rewrite(self, query, user_context=None):
        prompts = [
            # Step 1: 意图澄清
            f"用户问题: {query}\n用户意图是什么? 简述:",
            
            # Step 2: 同义词扩展
            f"问题: {query}\n生成3个同义表达:",
            
            # Step 3: 追问补全
            f"问题: {query}\n可能的补充信息:",
        ]
        
        # 简化的多步改写
        rewritten = self.llm.generate(
            "将问题改写成更清晰的搜索表达，"
            f"保留核心意图: {query}"
        )
        
        # 生成多个检索query
        queries = [
            query,  # 原问题
            rewritten,
            self._expand_with_synonyms(query),
        ]
        
        return queries
```

#### 2.2.3 Reranker 重排序

```python
# Cross-Encoder Reranker
from sentence_transformers import CrossEncoder

class CrossEncoderReranker:
    def __init__(self):
        self.model = CrossEncoder(
            'cross-encoder/ms-marco-MiniLM-L-12-v2'
        )
    
    def rerank(self, query, documents, top_k=5):
        """
        使用 Cross-Encoder 做精细化排序
        比向量检索更准确，但更慢
        """
        # 构造 query-document 对
        pairs = [(query, doc.text) for doc in documents]
        
        # 批量预测相关性分数
        scores = self.model.predict(pairs)
        
        # 按分数排序
        scored_docs = zip(documents, scores)
        sorted_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)
        
        return [doc for doc, _ in sorted_docs[:top_k]]
```

### 2.3 RAG 评估体系

```python
# RAGAs 评估指标
class RAGEvaluator:
    """
    RAGAs 评估框架核心指标
    """
    
    metrics = {
        # 检索质量
        'context_precision': "检索文档与问题的相关性",
        'context_recall': "检索文档覆盖答案的程度",
        'context_relevance': "检索上下文的精简程度",
        
        # 生成质量
        'answer_correctness': "答案准确性 (需ground truth)",
        'answer_faithfulness': "答案是否忠实于检索上下文",
        'answer_relevance': "答案对问题的相关性",
        
        # 端到端
        'response_quality': "综合回答质量",
    }
    
    def evaluate(self, question, answer, contexts, ground_truth=None):
        """完整评估"""
        results = {}
        
        # 计算各指标
        for metric_name in self.metrics:
            results[metric_name] = self._compute_metric(
                metric_name, question, answer, contexts, ground_truth
            )
        
        return results
```

### 2.4 RAG 常见问题与解决

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| **召回率低** | 分块太大/太小 | 优化分块策略，层次分块 |
| **精确率低** | 向量模型不匹配 | 微调 Embedding 模型 |
| **幻觉** | 上下文不完整 | 增加检索召回，添加强制引用 |
| **回答跳脱** | 缺少对话历史 | 添加 conversation history |
| **长文档处理** | 上下文溢出 | 摘要压缩，文档图索引 |

---

## 三、Agent 评估方法

### 3.1 Agent 评估维度

```
Agent 评估体系:

1. 任务完成度
   - 成功率 (Task Success Rate)
   - 步骤完成度
   - 结果正确性

2. 效率指标
   - 步数 (Number of Steps)
   - 工具调用次数
   - 执行时间

3. 质量指标
   - 响应质量
   - 规划合理性
   - 错误恢复能力

4. 安全指标
   - 有害内容检测
   - 敏感操作保护
   - 权限控制
```

### 3.2 主流 Agent 评估基准

| 基准 | 任务类型 | 指标 | 说明 |
|------|----------|------|------|
| **AgentBench** | 多行业任务 | 综合评分 | 清华出品 |
| **WebArena** | 网页操作 | 成功率 | 真实网站环境 |
| **MiniWob++** | 网页操作 | 任务完成率 | 简化版 WebArena |
| **ALFWorld** | 家庭任务 | 成功率 | 具身 AI |
| **ToolBench** | 工具调用 | 正确性 | API 调用 |
| **MINT-Bench** | 多模态工具 | 任务完成 | 视觉推理 |

### 3.3 评估实现示例

```python
class AgentEvaluator:
    def evaluate(self, agent, test_cases):
        results = []
        
        for case in test_cases:
            # 执行任务
            trajectory = agent.run(
                case.task,
                case.initial_state
            )
            
            # 计算指标
            metrics = {
                'success': self._check_success(trajectory, case.goal),
                'steps': len(trajectory.actions),
                'efficiency': 1 / len(trajectory.actions),  # 步数越少越好
                'safety': self._check_safety(trajectory),
                'faithfulness': self._check_faithfulness(trajectory),
            }
            
            results.append({
                'task_id': case.id,
                'metrics': metrics,
                'trajectory': trajectory,
            })
        
        # 聚合结果
        return self._aggregate_results(results)
```

---

## 四、LangChain/LangGraph 实战

### 4.1 LangGraph 核心概念

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next_action: str
    iteration: int
    memory: dict

# 定义节点
def analyze(state):
    """分析阶段"""
    last_message = state["messages"][-1]
    return {"next_action": "plan"}

def plan(state):
    """规划阶段"""
    plan = llm.plan(last_message)
    return {"messages": [plan], "iteration": state["iteration"] + 1}

def execute(state):
    """执行阶段"""
    action = state.get("current_plan")
    result = execute_action(action)
    return {"messages": [f"执行结果: {result}"]}

def reflect(state):
    """反思阶段"""
    reflection = llm.reflect(state["messages"])
    if reflection.needs_retry:
        return {"next_action": "plan"}
    return {"next_action": "finish"}

# 构建图
workflow = StateGraph(AgentState)

workflow.add_node("analyze", analyze)
workflow.add_node("plan", plan)
workflow.add_node("execute", execute)
workflow.add_node("reflect", reflect)

# 定义边
workflow.add_edge("analyze", "plan")
workflow.add_edge("plan", "execute")
workflow.add_edge("execute", "reflect")

def should_continue(state):
    return "plan" if state["next_action"] == "plan" else END

workflow.add_conditional_edges("reflect", should_continue)

# 编译
agent = workflow.compile()
```

### 4.2 工具调用实战

```python
from langchain.tools import tool
from langchain.agents import create_react_agent, AgentExecutor

# 定义工具
@tool
def search_codebase(query: str) -> str:
    """搜索代码库中的相关代码"""
    results = search(query)
    return format_results(results)

@tool
def read_file(path: str, start: int = 0, end: int = 100) -> str:
    """读取文件内容"""
    with open(path) as f:
        lines = f.readlines()[start:end]
    return "".join(lines)

@tool
def run_command(command: str) -> str:
    """执行 shell 命令"""
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    return result.stdout + result.stderr

# 构建 Agent
tools = [search_codebase, read_file, run_command]
agent = create_react_agent(llm, tools)

# 执行
executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10
)

result = executor.invoke({
    "input": "找到项目中的数据库连接代码，分析是否有SQL注入风险"
})
```

### 4.3 Memory 管理

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph

# 带 Memory 的 Agent
checkpointer = MemorySaver()

workflow = StateGraph(AgentState, checkpointer=checkpointer)
# ... 添加节点和边 ...

agent = workflow.compile()

# 带 checkpoint 执行
config = {"configurable": {"thread_id": "user_123"}}

# 第一次对话
result1 = agent.invoke(
    {"messages": [HumanMessage(content="我叫张三")]},
    config=config
)

# 第二次对话（记住张三）
result2 = agent.invoke(
    {"messages": [HumanMessage(content="我叫什么名字？")]},
    config=config
)
# result2 会记住 "张三"
```

---

## 五、Agent 生产最佳实践

### 5.1 生产部署检查清单

```
✅ Agent 生产检查清单:

1. 可靠性
   □ 超时处理 (单步超时、整体超时)
   □ 重试机制 (指数退避)
   □ 熔断保护 (失败率 > 阈值则暂停)

2. 安全性
   □ 权限控制 (最小权限原则)
   □ 敏感操作二次确认
   □ 输入输出过滤
   □ SQL/命令注入防护

3. 可观测性
   □ 完整日志记录
   □ 追踪每个决策点
   □ 关键指标监控
   □ 异常告警

4. 成本控制
   □ Token 使用量统计
   □ 工具调用计费
   □ 缓存策略
   □ 模型降级方案

5. 版本管理
   □ Prompt 版本控制
   □ 工具版本锁定
   □ 灰度发布
   □ 快速回滚
```

### 5.2 错误处理模式

```python
class ResilientAgent:
    def __init__(self, agent, max_retries=3):
        self.agent = agent
        self.max_retries = max_retries
    
    def run_with_retry(self, task):
        for attempt in range(self.max_retries):
            try:
                return self.agent.run(task)
            except ToolTimeoutError:
                logger.warning(f"Attempt {attempt+1} timeout")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
            except ToolPermissionError:
                logger.error("Permission denied")
                return self._generate_permission_error_response()
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return self._generate_fallback_response()
        
        return self._generate_max_retries_exceeded_response()
    
    def run_with_circuit_breaker(self, task):
        if self.circuit_breaker.is_open:
            logger.warning("Circuit breaker open, using fallback")
            return self._fallback_response(task)
        
        try:
            result = self.run_with_retry(task)
            self.circuit_breaker.record_success()
            return result
        except Exception:
            self.circuit_breaker.record_failure()
            raise
```

### 5.3 性能优化技巧

```python
# 1. 工具调用并行化
async def parallel_tool_calls(tools, params):
    tasks = [tool.ainvoke(p) for tool, p in zip(tools, params)]
    return await asyncio.gather(*tasks)

# 2. 流式响应
async def stream_response(query, agent):
    async for chunk in agent.astream(query):
        yield chunk  # 逐 token 输出

# 3. 结果缓存
@lru_cache
def cached_retrieval(query_hash):
    return vector_search(query_hash)

# 4. Prompt 压缩
def compress_context(long_context):
    return llm.summarize(
        f"压缩以下上下文，保留关键信息:\n{long_context}"
    )
```

---

## 六、面试高频问题

### Q1: 如何设计一个可靠的多步 Agent 系统？

**参考答案**:

设计要点：

```
1. 状态机设计
   - 清晰的阶段划分 (分析→规划→执行→反思)
   - 有限状态转换
   - 状态持久化 (断点恢复)

2. 错误处理
   - 每步超时保护
   - 失败重试 + 指数退避
   - 熔断器防止雪崩

3. 可观测性
   - 完整执行轨迹记录
   - 决策点日志
   - 关键指标监控

4. 降级策略
   - 模型降级 (大→小)
   - 功能降级 (Agent→规则)
   - 快速失败
```

### Q2: RAG 和 Fine-tuning 如何选择？

**参考答案**:

| 场景 | 推荐方案 | 原因 |
|------|----------|------|
| **知识快速更新** | RAG | 无需重新训练 |
| **特定领域术语** | Fine-tuning | 学会领域表达 |
| **需要溯源** | RAG | 天然可引用 |
| **格式/风格一致性** | Fine-tuning | 学习输出格式 |
| **成本敏感** | RAG | 训练成本高 |
| **最新信息** | RAG | 实时检索 |
| **复杂推理模式** | Fine-tuning | 学习推理链 |

**最优解**: RAG + Fine-tuning 结合

```python
# 组合策略
if needs_knowledge:
    # 知识密集 → RAG
    context = retrieve(query)
    answer = generate(query, context)
elif needs_style:
    # 风格/格式 → Fine-tuned
    answer = fine_tuned_model.generate(query)
else:
    # 两者都需要 → 组合
    context = retrieve(query)
    answer = fine_tuned_model.generate(query, context)
```

### Q3: Agent 如何避免陷入死循环？

**参考答案**:

```
1. 状态去重
   - 记录已访问状态
   - 遇到重复状态则终止

2. 步数限制
   - 设置最大迭代次数
   - 超限则强制结束

3. 自我检测
   - 每步检查"是否在进步"
   - 相似结果连续出现则终止

4. 规划审查
   - 执行前审查计划可行性
   - 不可行则调整策略
```

```python
def should_continue(state, max_steps=20):
    # 检查步数
    if len(state.history) > max_steps:
        return False
    
    # 检查重复
    if state.current_result in state.past_results:
        return False
    
    # 检查进度
    if not is_making_progress(state):
        return False
    
    return True
```

### Q4: 如何评估 Agent 的效果？

**参考答案**:

分层评估：

```
1. 任务层
   - 成功率 (Task Success)
   - 步骤数 (效率)
   - 成本 (Token 消耗)

2. 决策层
   - 规划质量 (是否最优路径)
   - 工具选择准确率
   - 错误恢复能力

3. 输出层
   - 答案质量
   - 引用准确性
   - 安全性
```

常用基准：**AgentBench, WebArena, ToolBench**

### Q5: 生产环境 Agent 的成本如何优化？

**参考答案**:

```
1. 推理优化
   - 小模型处理简单任务
   - 级联模型 (快→慢)
   - 批处理合并请求

2. 检索优化
   - 结果缓存
   - 向量量化
   - 召回量控制

3. 数据优化
   - Prompt 压缩
   - 上下文截断
   - 摘要替换原文

4. 架构优化
   - 流式响应
   - 异步处理
   - 缓存中间结果
```

---

## 参考资料

1. Yao et al. - "ReAct: Synergizing Reasoning and Acting in Language Models" (2022)
2. Shinn et al. - "Reflexion: Language Agents with Verbal Reinforcement Learning" (2023)
3. Wei et al. - "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (2022)
4. LangChain Documentation - https://docs.langchain.com
5. LangGraph Documentation - https://langchain-ai.github.io/langgraph/
6. AgentBench - https://agentbench.github.io/

---

*本章持续更新，关注 Agent 系统最新进展*
