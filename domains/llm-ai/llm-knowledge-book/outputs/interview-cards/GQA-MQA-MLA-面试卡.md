# 面试卡：MHA / MQA / GQA / MLA

## 高频问法

- MHA、MQA、GQA 差在哪？
- GQA 为什么能减少 KV Cache？
- MLA 和 GQA 有什么区别？

## 30 秒回答

MHA 是每个 Query 头都有独立 K/V，表达强但 KV Cache 大。MQA 是所有 Query 头共享一组 K/V，最省显存但可能影响质量。GQA 是把 Query 头分组，每组共享一组 K/V，是现代 LLM 常见折中。MLA 则用低秩 latent 压缩 KV，进一步降低缓存成本。

## 2 分钟回答

推理时 KV Cache 大小和 KV 头数量强相关。MHA 中 `num_kv_heads = num_q_heads`，所以缓存最大。MQA 把 KV 头降到 1，显存最低，但所有 Q 头共享同一份 K/V，表达可能受影响。GQA 让多个 Q 头共享一组 K/V，比如 32 个 Q 头配 8 个 KV 头，每 4 个 Q 头共享一组 KV。MLA 更进一步，不直接缓存完整 K/V，而是缓存低维 latent，需要时再解压。

## 追问

### Q1：GQA 减少的是 Q 头吗？

回答：不是，主要减少 KV 头数量，Q 头仍然可以保持较多。

### Q2：为什么 MQA 不一定最好？

回答：KV 极致共享可能损失不同头的表达多样性，GQA 在质量和成本之间更平衡。

### Q3：MLA 的关键是什么？

回答：关键是低秩压缩缓存，不只是减少 KV head。

## 容易翻车

- 错误：GQA 是为了让模型更聪明。
- 正确：主要动机之一是降低推理时 KV Cache 成本。

