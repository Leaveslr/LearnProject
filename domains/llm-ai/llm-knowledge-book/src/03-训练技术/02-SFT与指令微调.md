# SFT 与指令微调

> 目标：理解 SFT 在 LLM 训练链路中的位置，以及它和预训练、RLHF/DPO 的区别。

## 一句话结论

SFT 不是教模型“学会语言”，而是用高质量指令数据把预训练模型对齐到用户期望的交互格式和任务行为。

## 1. LLM 训练链路

```text
预训练 -> SFT -> 偏好对齐(RLHF/DPO/GRPO) -> 安全/领域微调 -> 评估部署
```

不同阶段目标不同：

| 阶段 | 数据 | 目标 |
| --- | --- | --- |
| 预训练 | 大规模无标注文本 | 学语言、知识、模式 |
| SFT | 指令-回答样本 | 学会按指令回答 |
| RLHF/DPO | 偏好数据 | 学会更符合人类偏好 |
| 领域微调 | 领域问答/任务数据 | 适配特定业务 |

## 2. SFT 数据格式

常见数据结构：

```json
{
  "instruction": "解释 KV Cache 的作用",
  "input": "",
  "output": "KV Cache 用于缓存历史 token 的 Key/Value..."
}
```

多轮对话格式：

```json
[
  {"role": "system", "content": "你是一个专业算法工程师"},
  {"role": "user", "content": "什么是 LoRA？"},
  {"role": "assistant", "content": "LoRA 是一种参数高效微调方法..."}
]
```

## 3. Chat Template

Chat template 把结构化对话转换成模型训练用的 token 序列：

```text
<|system|>...
<|user|>...
<|assistant|>...
```

不同模型的 template 不同，SFT 时必须和目标模型的格式匹配。

## 4. Loss Masking

SFT 通常只对 assistant 的回答部分计算 loss，不对用户 prompt 计算 loss：

```text
system/user tokens -> label = -100
assistant tokens   -> label = token_id
```

原因：我们希望模型学习如何回答，而不是学习复述用户输入。

## 5. 数据质量

SFT 效果高度依赖数据质量。

关键维度：

- 指令多样性。
- 回答准确性。
- 格式一致性。
- 难度分层。
- 安全边界。
- 领域覆盖。

常见数据问题：

- 回答啰嗦但没信息。
- 指令和回答不匹配。
- 多轮对话上下文断裂。
- 数据泄露 benchmark。
- 过多模板化回答导致模型僵硬。

## 6. SFT 与 LoRA

SFT 是训练目标或阶段，LoRA 是参数高效训练方法。两者不是同一维度。

可以：

- 全量 SFT。
- LoRA SFT。
- QLoRA SFT。

选择依据：

| 场景 | 建议 |
| --- | --- |
| 资源充足、任务重要 | 全量 SFT |
| 中小规模领域适配 | LoRA SFT |
| 消费级 GPU | QLoRA SFT |
| 只调格式和轻量行为 | LoRA / Prefix Tuning |

## 7. SFT 的局限

SFT 学的是示范数据分布，不能直接表达“两个回答哪个更好”的偏好。

局限：

- 需要大量高质量示范。
- 对偏好和安全边界学习有限。
- 容易学到数据中的口癖和格式偏差。
- 很难优化主观质量，如有帮助、简洁、诚实。

因此后续常接 RLHF、DPO、GRPO 等偏好对齐方法。

## 面试追问

### Q1：SFT 和预训练的区别？

回答：预训练用大规模无标注文本学习语言和知识，SFT 用指令-回答数据让模型学会按用户意图完成任务。

### Q2：为什么 SFT 通常只对 assistant 输出算 loss？

回答：用户和 system 部分是条件上下文，不是模型要学习生成的目标；只对 assistant 部分算 loss 能让模型专注学习回答行为。

### Q3：SFT 后为什么还要 RLHF/DPO？

回答：SFT 只能模仿示范答案，偏好对齐能学习人类对多个候选回答的相对偏好，更适合优化帮助性、安全性和主观质量。

## 内容选题

- 小红书：SFT、LoRA、RLHF 到底是不是一回事？
- 视频：为什么指令微调能让模型变得“听话”？
- 面试：SFT 数据怎么构造才有效？
