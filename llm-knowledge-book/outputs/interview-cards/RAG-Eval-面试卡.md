# 面试卡：RAG 评估

## 高频问法

- RAG 答错怎么排查？
- RAG 评估有哪些指标？
- LLM-as-judge 有什么风险？

## 30 秒回答

RAG 评估要分层：先看检索是否召回正确文档，再看传给模型的 context 是否包含答案且不冗余，最后看生成是否忠实、有引用、事实正确。不能只看最终答案，否则无法定位是检索、rerank、prompt 还是生成问题。

## 2 分钟回答

我会把 RAG 评估拆成三层。检索层看 Recall@k、MRR、nDCG、Hit Rate，确认正确资料是否被找出来。上下文层看 Context Recall、Context Precision、Relevance、冗余率，确认进入 prompt 的内容是否足够且干净。答案层看 Faithfulness、Factual Correctness、Citation Accuracy 和用户满意度。线上还要监控无答案率、检索空结果率、人工转接率、延迟和 token 成本。评估集要有 easy、hard、adversarial 和 regression 样本。

## 追问

### Q1：答案错了先查哪里？

回答：先看检索是否召回正确文档，再看 rerank/context，最后看模型是否忠实生成。

### Q2：LLM-as-judge 风险？

回答：可能有长度偏好、位置偏好和不稳定性，需要清晰 rubric、人工校准和抽检。

### Q3：golden set 怎么建？

回答：从真实问题、业务高频、历史失败和对抗样本中分层采样，记录 expected answer、sources、tags、failure mode。

## 容易翻车

- 错误：RAG 错了就是模型幻觉。
- 正确：必须先定位检索和上下文链路。

