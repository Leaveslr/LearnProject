# LLM / RAG / Agent 评估体系

> 目标：把“模型好不好”拆成可观测、可复现、可迭代的指标体系。

## 一句话结论

LLM 应用评估不能只看模型分数，必须把基础模型能力、RAG 检索质量、生成忠实性、Agent 任务成功率和线上反馈分开评估。

## 1. 为什么评估要分层

一个 RAG Agent 回答错，可能来自：

- 基础模型能力不足。
- 用户问题理解错。
- query rewrite 错。
- 检索没召回。
- rerank 排错。
- prompt 组织差。
- 生成幻觉。
- 工具调用失败。
- 业务规则不完整。

如果只看最终答案，就无法定位问题。

## 2. LLM 基础评估

常见指标：

| 指标 | 说明 | 局限 |
| --- | --- | --- |
| Perplexity | 语言建模困惑度 | 不代表任务质量 |
| Accuracy | 客观题准确率 | 依赖 benchmark |
| Pass@k | 代码题通过率 | 需要可执行测试 |
| Win rate | A/B 回答偏好 | 评审标准可能漂移 |
| LLM-as-judge | 用模型评审 | 需要校准和抽检 |

评估原则：

- 构建固定 golden set。
- 区分自动评估和人工评估。
- 保留错误样本和原因标签。
- 防止 benchmark contamination。

## 3. RAG 评估

RAG 至少分三层：

```text
检索评估 -> 上下文评估 -> 答案评估
```

### 检索评估

关注是否把正确文档召回：

- Recall@k
- Precision@k
- MRR
- nDCG
- Hit Rate

### 上下文评估

关注传给 LLM 的 context 是否足够：

- Context Recall
- Context Precision
- Context Relevance
- 冗余率

### 答案评估

关注生成结果：

- Answer Relevance
- Faithfulness
- Factual Correctness
- Citation Accuracy
- 用户满意度

## 4. Agent 评估

Agent 评估不能只看最终文本，需要看轨迹：

| 层级 | 指标 |
| --- | --- |
| 任务结果 | success rate、completion rate |
| 工具调用 | tool accuracy、参数正确率、调用次数 |
| 轨迹质量 | 是否走弯路、是否循环、是否违反约束 |
| 成本延迟 | token cost、wall time、tool latency |
| 安全 | 越权调用、敏感信息泄露、prompt injection |

建议保存 trace：

```text
user input -> planning -> tool calls -> observations -> final answer
```

## 5. 评估数据集

评估集建议分层构建：

- Easy：基础功能正常。
- Hard：长上下文、多跳、模糊问题。
- Adversarial：注入攻击、无答案问题、冲突文档。
- Regression：历史线上失败案例。

每条样本建议记录：

```yaml
id:
user_query:
expected_answer:
expected_sources:
tags:
failure_modes:
priority:
```

## 6. 线上监控

上线后关注：

- 用户满意度。
- 人工转接率。
- 无答案率。
- 检索空结果率。
- 工具调用失败率。
- 平均延迟。
- token 成本。
- 安全拦截率。

## 7. 常见误区

- **误区 1：只看大模型 benchmark。** 应用效果更多取决于数据、检索、prompt、工具和业务闭环。
- **误区 2：只用 LLM-as-judge。** 模型评审需要人工抽检和一致性校准。
- **误区 3：只评最终答案。** Agent 必须评估工具调用轨迹和中间决策。

## 面试追问

### Q1：RAG 答案错了怎么排查？

回答：先看检索是否召回正确文档，再看 rerank 和 context 是否包含答案，最后看模型是否忠实生成。不要直接归因于模型幻觉。

### Q2：如何评估 Agent？

回答：分任务成功率、工具调用准确率、轨迹质量、成本延迟和安全约束评估，并保存 trace 做错误归因。

### Q3：LLM-as-judge 有什么风险？

回答：可能有偏见、长度偏好、位置偏好和不稳定性，需要清晰 rubric、少量人工标注校准和定期抽检。

## 内容选题

- 小红书：RAG 效果差，到底该怪检索还是模型？
- 视频：Agent 不能只看最终答案，trace 才是关键
- 面试：如何设计一个 LLM 应用评估体系？
