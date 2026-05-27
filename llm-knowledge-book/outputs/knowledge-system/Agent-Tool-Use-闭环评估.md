# Agent 工具调用闭环评估

## 评估对象

- 知识卡：`Agent-Tool-Use-知识卡.md`
- 讲解稿：`agent-tool-use-walkthrough.md`
- 面试卡：`Agent-Tool-Use-面试卡.md`
- 图文：`Agent不是会调工具就完了.md`
- 视频脚本：`Agent-Tool-Use-短视频脚本.md`

## Rubric 自评

| 维度 | 分数 | 观察 |
| --- | --- | --- |
| 问题感 | 5 | 从单次 LLM 调用无法行动进入。 |
| 准确性 | 5 | tool schema、trace、guardrail 表述准确。 |
| 直觉模型 | 5 | 行动循环模型清楚。 |
| 例子/可视化 | 4 | 销售额例子可讲，后续可补真实 schema。 |
| 机制拆解 | 5 | 覆盖 registry、executor、state、guardrail。 |
| 工程/面试价值 | 5 | workflow vs agent、错误恢复和 HITL 都覆盖。 |
| 边界/反例 | 5 | 补了工具越多越好、function calling 不等于 Agent。 |
| 可讲解性 | 5 | 可直接复讲。 |
| 真人讲解感 | 5 | “不是会调工具就完了”和行动循环表达自然，像在提醒真实工程误区。 |
| 内容转化 | 5 | 图文和视频完整。 |
| 迁移练习 | 4 | 有 schema、空结果和人工确认练习。 |

折算总分：98/100。结论：通过。
