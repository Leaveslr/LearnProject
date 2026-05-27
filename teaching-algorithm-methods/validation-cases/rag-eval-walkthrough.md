# 流程走样例：RAG 评估

## 目标

把 RAG 评估讲成可排障链路，而不是只列指标。

## 1. 问题场景

RAG 答错时，常见反应是“模型幻觉”。但真正原因可能在检索、rerank、context、prompt 或生成。

## 2. 直觉模型

RAG 像开卷考试：

- 检索：有没有找到正确资料。
- 上下文：有没有把正确资料放进试卷。
- 生成：有没有按资料回答。

## 3. 最小例子

问题：“报销上限是多少？”

- 没召回制度：检索失败。
- 召回了但上下文没放答案段：context 失败。
- context 有答案但模型编了：faithfulness 失败。

## 4. 机制拆解

```text
检索评估 -> 上下文评估 -> 答案评估 -> 线上监控
```

- 检索：Recall@k、MRR、nDCG。
- 上下文：Context Recall、Relevance、冗余率。
- 答案：Faithfulness、Citation Accuracy、Factual Correctness。
- 线上：无答案率、人工转接率、延迟、成本。

## 5. 工程取舍

- Golden set 要覆盖 easy/hard/adversarial/regression。
- LLM-as-judge 要配人工抽检。
- 错误样本要打 failure mode 标签。

## 6. 易错点和反例

- 错误：Recall 高答案一定好。反例：上下文冗余、模型仍可能幻觉。
- 错误：只评最终答案。反例：无法定位是检索还是生成错。
- 错误：judge 模型绝对可靠。反例：有长度偏好和不稳定性。

## 7. 迁移练习

- 设计一个客服 RAG 的 golden set 字段。
- 一个答案有引用但引用不支持结论，该算什么错误？
- 如果检索空结果率升高，优先查哪里？

