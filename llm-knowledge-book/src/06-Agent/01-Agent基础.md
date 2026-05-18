# 第七章：AI Agent 基础概念

## 7.1 什么是 AI Agent？

### 7.1.1 Agent 定义

AI Agent（智能体）是能够**感知环境、自主决策、执行动作**的智能系统。与简单的 LLM 调用不同，Agent 具有：

```
┌─────────────────────────────────────────────────────────────┐
│                      AI Agent 核心能力                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 感知 (Perception)                                       │
│     - 理解用户输入                                          │
│     - 解析工具返回结果                                       │
│     - 维护对话上下文                                        │
│                                                              │
│  2. 推理 (Reasoning)                                        │
│     - 分析任务目标                                          │
│     - 制定执行计划                                          │
│     - 评估当前状态                                          │
│                                                              │
│  3. 行动 (Action)                                           │
│     - 调用外部工具                                          │
│     - 与环境交互                                            │
│     - 响应用户                                              │
│                                                              │
│  4. 记忆 (Memory)                                           │
│     - 短期记忆：当前会话上下文                               │
│     - 长期记忆：历史经验知识                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 7.1.2 Agent vs 简单 LLM 调用

| 特性 | 简单 LLM 调用 | AI Agent |
|------|--------------|----------|
| **交互方式** | 单轮问答 | 多轮循环 |
| **工具使用** | 不支持 | 支持 |
| **自主性** | 低 | 高 |
| **目标导向** | 否 | 是 |
| **自我反思** | 不支持 | 支持 |

---

## 7.2 Agent 的核心组件

### 7.2.1 Agent 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Agent 系统架构                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                      用户输入                                 │
│                         │                                   │
│                         ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              工具注册表 (Tools Registry)              │   │
│  │    search_web | calculator | code_exec | database    │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    LLM (大脑)                         │   │
│  │                                                      │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐              │   │
│  │  │ 思考    │→│ 决策    │→│ 行动    │              │   │
│  │  │(Thought)│  │(Decide) │  │(Action) │              │   │
│  │  └─────────┘  └─────────┘  └─────────┘              │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│          ┌──────────────┼──────────────┐                    │
│          ▼              ▼              ▼                    │
│   ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│   │ 短期记忆   │  │ 长期记忆   │  │  工具执行   │          │
│   │ (Context)  │  │ (Memory)  │  │ (Execute) │          │
│   └────────────┘  └────────────┘  └────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 7.2.2 组件详解

| 组件 | 功能 | 实现方式 |
|------|------|---------|
| **工具注册** | 定义可调用的外部能力 | MCP、Function Calling |
| **推理引擎** | LLM 负责思考和决策 | Prompt Engineering |
| **短期记忆** | 当前任务上下文 | 对话历史、变量状态 |
| **长期记忆** | 跨会话知识存储 | 向量数据库、KG |
| **执行器** | 调用工具并获取结果 | API 调用、代码执行 |

---

## 7.3 ReAct 范式

### 7.3.1 ReAct 核心思想

ReAct = **Reason** + **Act**：让 Agent 交替进行推理和行动。

```
Thought: 我需要先搜索相关信息
Action: search_web(query="...")
Observation: 搜索结果显示...
Thought: 搜索结果中提到...
Action: calculator(...)
Observation: 计算结果...
Thought: 现在我有足够信息回答
Action: respond(...)
```

### 7.3.2 ReAct 代码实现

```python
from typing import List, Dict, Callable

class ReActAgent:
    def __init__(self, llm, tools: Dict[str, Callable]):
        self.llm = llm
        self.tools = tools
        self.tools_desc = "\n".join([
            f"{name}: {tool.__doc__}" 
            for name, tool in tools.items()
        ])
    
    def run(self, task: str, max_iterations: int = 10) -> str:
        """执行 ReAct 循环"""
        context = []
        
        system_prompt = f"""你是一个智能助手。
可用的工具：
{self.tools_desc}

每次回复使用以下格式：
Thought: <你的思考>
Action: <工具名>(<参数>)
Observation: <执行结果>

当任务完成时，回复：
Final Answer: <最终回答>
"""
        
        for i in range(max_iterations):
            # 调用 LLM
            response = self.llm.chat([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": task},
                {"role": "assistant", "content": "\n".join(context)},
            ])
            
            if "Final Answer:" in response:
                return response.split("Final Answer:")[1].strip()
            
            # 解析并执行
            thought = self.extract("Thought:", response)
            action = self.extract("Action:", response)
            
            # 执行工具
            result = self.execute(action)
            context.append(f"Thought: {thought}\nAction: {action}\nObservation: {result}")
        
        return "达到最大迭代次数"
```

---

## 7.4 Agent 开发框架

### 7.4.1 主流框架对比

| 框架 | 特点 | 适用场景 |
|------|------|---------|
| **LangChain** | 全能型，生态丰富 | 快速原型 |
| **LangGraph** | 图结构，支持复杂流程 | 多 Agent 协作 |
| **LlamaIndex** | 数据连接强 | RAG 场景 |
| **CrewAI** | 多 Agent 协作 | 团队协作任务 |
| **AutoGen** | Microsoft 出品 | 企业应用 |
| **Dify** | 低代码 | 快速上线 |

### 7.4.2 LangGraph 入门

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    next_action: str

def should_continue(state: AgentState) -> str:
    """决定是否继续"""
    if len(state["messages"]) > 10:
        return "end"
    return "continue"

def agent_node(state: AgentState) -> AgentState:
    """Agent 决策节点"""
    response = llm.invoke(state["messages"])
    return {"messages": [response], "next_action": "execute_tool"}

def execute_tool_node(state: AgentState) -> AgentState:
    """工具执行节点"""
    # 执行工具逻辑
    return {"messages": []}

# 构建图
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("execute_tool", execute_tool_node)
graph.add_edge("__start__", "agent")
graph.add_conditional_edges("agent", should_continue, {
    "continue": "execute_tool",
    "end": END
})
graph.add_edge("execute_tool", "agent")

app = graph.compile()
```

---

## 7.5 Agent 的记忆系统

### 7.5.1 短期记忆

处理当前会话的信息：

```python
class ShortTermMemory:
    """滑动窗口短期记忆"""
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.history = []
    
    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        # 滑动窗口
        if len(self.history) > self.max_turns:
            self.history = self.history[-self.max_turns:]
    
    def get_context(self) -> str:
        return "\n".join([
            f"{m['role']}: {m['content']}" 
            for m in self.history
        ])
```

### 7.5.2 长期记忆

跨会话存储知识：

```python
class LongTermMemory:
    """基于向量数据库的长期记忆"""
    def __init__(self, vector_store):
        self.vector_store = vector_store
    
    def store(self, content: str, metadata: dict):
        """存储记忆"""
        embedding = embed_model.encode(content)
        self.vector_store.add(
            vectors=[embedding],
            documents=[content],
            metadatas=[metadata]
        )
    
    def recall(self, query: str, top_k: int = 5) -> list:
        """召回相关记忆"""
        query_embedding = embed_model.encode(query)
        results = self.vector_store.search(
            query_vectors=[query_embedding],
            top_k=top_k
        )
        return results["documents"][0]
```

---

## 7.6 工具调用（Function Calling）

### 7.6.1 OpenAI Function Calling

```python
import openai

functions = [
    {
        "name": "get_weather",
        "description": "获取指定城市的天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称"
                }
            },
            "required": ["city"]
        }
    }
]

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "北京今天天气怎么样？"}],
    tools=[{"type": "function", "function": f} for f in functions],
    tool_choice="auto"
)

# 解析工具调用
tool_calls = response.choices[0].message.tool_calls
for call in tool_calls:
    if call.function.name == "get_weather":
        args = json.loads(call.function.arguments)
        weather = get_weather(city=args["city"])
```

---

## 7.7 面试高频问题

### Q1: 什么是 ReAct 范式？

> ReAct 是"Reasoning + Acting"的结合，让 Agent 在推理和行动之间交替进行。通过显式的"Thought"步骤，让模型先分析情况，再决定行动，提高决策质量。

### Q2: Agent 的记忆系统怎么设计？

> 通常分为短期记忆（当前会话的滑动窗口）和长期记忆（向量数据库存储的历史经验）。短期记忆用于当前任务上下文，长期记忆用于跨会话知识复用。

### Q3: 如何防止 Agent 陷入死循环？

> 1. 设置最大迭代次数
> 2. 记录已执行的工具调用，避免重复
> 3. 在 prompt 中明确任务目标
> 4. 添加自我反思节点，检查是否完成任务

### Q4: 多 Agent 系统如何协作？

> 常见模式：
> - **分层协作**：领导 Agent 分解任务，执行 Agent 处理子任务
> - **对抗协作**：多个 Agent 辩论，取最优方案
> - **流水线**：串联执行，每个 Agent 处理特定阶段

---

*参考文献*
- Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", 2022
- https://github.com/aceliuchanghong/FAQ_Of_LLM_Interview
