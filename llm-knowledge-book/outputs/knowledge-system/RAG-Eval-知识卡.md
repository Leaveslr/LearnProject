# 知识卡：RAG 评估

## 资料来源

- 主笔记：[LLM / RAG / Agent 评估体系](../../src/08-评估与安全/01-LLM-RAG-Agent评估体系.md)

## 一句话结论

RAG 评估不能只看最终回答，要分开评估检索是否召回、上下文是否有用、生成是否忠实。

## 它解决什么问题

- RAG 答错可能是检索、rerank、prompt、生成或数据问题。
- 只看最终答案无法定位失败环节。
- 分层评估能把“效果差”变成可排查的问题。

## 核心直觉

RAG 像开卷考试：

- 检索：有没有把正确资料找出来。
- 上下文：有没有把有用资料放到卷面上。
- 生成：有没有根据资料忠实作答。

## 最小例子

用户问：“公司报销上限是多少？”

- 没召回制度文档：检索失败。
- 召回了但没放进 context：上下文失败。
- context 有答案但模型编了一个：生成忠实性失败。

## 关键机制

- 检索评估：Recall@k、Precision@k、MRR、nDCG、Hit Rate。
- 上下文评估：Context Recall、Context Precision、Relevance、冗余率。
- 答案评估：Faithfulness、Factual Correctness、Citation Accuracy、满意度。

## 工程应用

- 建 golden set。
- 给失败样本打标签。
- 做 regression set 防止版本回退。
- 线上监控无答案率、检索空结果率、人工转接率、延迟和成本。

## 常见误区

- RAG 错了就怪模型幻觉。
- 只用 LLM-as-judge。
- 只评最终答案，不看中间 context。

## 边界和反例

- 检索指标高不代表答案好，可能 context 太冗余。
- 答案流畅不代表忠实。
- judge 模型可能有长度偏好和位置偏好。

## 面试追问

- RAG 答错怎么排查？
- 如何构建 golden set？
- LLM-as-judge 有什么风险？

## 内容转化角度

- 小红书：RAG 效果差，到底怪谁？
- 短视频：三层拆 RAG 评估。
- 面试卡：检索、上下文、答案、线上监控一起答。

## 迁移练习

- 同型：给一个失败样本标注 failure mode。
- 变式：设计一个客服 RAG 评估集。
- 判断：Recall@k 高就代表 RAG 好吗？

