---
type: note
status: literature
created: 2026-04-29
source: https://arxiv.org/abs/2603.23420
paper: ../Papers/Bilevel Autoresearch Meta-Autoresearching Itself.pdf
tags:
  - AI
  - autoresearch
  - agent
  - meta-learning
  - paper
---

# Bilevel Autoresearch Meta-Autoresearching Itself

一句话：
这篇论文提出让 Autoresearch 研究 Autoresearch 自己：内层循环优化任务结果，外层循环优化内层循环的搜索机制，并通过运行时生成和注入 Python 代码来改变搜索方式。

## 本地资料

- PDF：[[Bilevel Autoresearch Meta-Autoresearching Itself.pdf|本地 PDF]]
- arXiv：https://arxiv.org/abs/2603.23420
- HTML：https://arxiv.org/html/2603.23420v1
- 代码：https://github.com/EdwardOptimization/Bilevel-Autoresearch

## 论文要解决的问题

普通 Autoresearch 已经可以让 LLM 做“提出假设、修改代码、运行实验、评估结果、保留或丢弃”的循环，但它有一个关键限制：搜索机制是人类提前写死的。

也就是说，LLM 可以在既定规则内做实验，但不能自己改进“做实验的方法”。这篇论文问的是：

- 能不能让 LLM 阅读 Autoresearch 系统本身的代码？
- 能不能让 LLM 发现内层搜索循环的瓶颈？
- 能不能让 LLM 自己写新的搜索机制代码，并注入到运行中的系统里？

论文的答案是：可以。核心思路就是 Bilevel Autoresearch。

## 整体框架

论文把系统分成三层：

```text
Level 2   机制研究层
          研究“内层循环应该如何搜索”，生成并注入新的 Python 搜索机制
             ↓
Level 1.5 搜索策略调节层
          根据最近实验轨迹冻结/解冻参数，并给内层循环注入搜索指导
             ↓
Level 1   内层 Autoresearch 循环
          修改 train.py 参数，训练 300 秒，比较 val_bpb，保留或丢弃变化
```

最重要的区分是：

- Level 1 优化任务本身。
- Level 1.5 调整现有搜索策略的参数。
- Level 2 改变搜索机制本身。

所以这篇论文真正的新意在 Level 2。它不是告诉 LLM “多试试学习率”，而是让 LLM 写一个新的搜索器，例如 Tabu Search、Bandit Proposer 或 Orthogonal Exploration，直接改变内层循环产生候选方案的方式。

## 主流程

一次完整流程大致是：

1. 从 baseline `train.py` 开始。
2. Level 1 让 LLM 提出一个参数改动和一句假设。
3. 系统把改动应用到工作副本，训练固定 300 秒。
4. 如果 `val_bpb` 变好，就保留这个改动；否则丢弃。
5. 每 5 次内层迭代，Level 1.5 分析历史实验，更新冻结参数和搜索指导。
6. 每 2 个外层周期，Level 2 读取 `runner.py` 和搜索轨迹，进行一次 4 轮机制研究会话。
7. Level 2 生成新的 Python 搜索机制，并 patch 到 `runner.py`。
8. 系统用 `importlib` 动态加载验证新代码。
9. 如果导入成功，新机制生效；如果失败，恢复原始 runner。
10. 系统继续运行内层实验循环。

## Level 1：内层 Autoresearch 循环

功能：
负责真正做实验，目标是优化 GPT 预训练 benchmark 上的 `val_bpb`。

输入：

- 当前最好的 `train.py`。
- 可以编辑的参数列表。
- 已冻结的参数列表。
- Level 1.5 注入的搜索指导。

动作：

- LLM 提出一组参数修改。
- LLM 给出一句假设，说明为什么这个改动可能有效。
- 系统运行训练，预算固定为 300 秒。
- 如果指标更好，保留；否则回滚。

特点：

- 它像一个 LLM 引导的 hill climbing。
- 它很容易重复自己的先验偏好。
- 在论文实验里，纯 Level 1 会反复尝试相似方向，出现连续丢弃。

例子：

```text
当前最好配置：
TOTAL_BATCH_SIZE = 524288
WEIGHT_DECAY = 0.1

Level 1 提案：
把 WEIGHT_DECAY 降到 0.05

假设：
较低的 weight decay 可能减少欠拟合。

训练 300 秒：
val_bpb 下降，说明变好。

结果：
保留这次修改。
```

## Level 1.5：搜索策略调节层

功能：
它不写新机制，只调节内层搜索策略，让内层循环少在无效参数上打转。

触发频率：
每 5 次 Level 1 迭代执行一次。

输入：

- 完整 proposal history。
- 每次实验的结果。
- 哪些参数反复尝试但没有收益。

输出：

- 冻结某些参数。
- 解冻某些参数。
- 给内层循环一段 guidance，例如“优先探索未充分尝试的参数”。

它能做什么：

- 发现某些参数一直没收益，就暂时冻结。
- 发现搜索卡住，就引导模型换方向。
- 增加搜索多样性。

它不能做什么：

- 不能改变 proposal 生成逻辑。
- 不能改变 keep/discard 接受规则。
- 不能改变整个循环结构。

论文结论：
Level 1.5 能让搜索更分散，但单独使用时收益不稳定。它更像“方向提醒器”，不是根本机制创新。

例子：

```text
过去 5 次实验：
WINDOW_PATTERN 改了 3 次，没有带来提升。
WEIGHT_DECAY 改了 2 次，也没有提升。

Level 1.5 决策：
冻结 WINDOW_PATTERN 和 WEIGHT_DECAY。
指导语：
接下来优先探索 LR、UNEMBEDDING_LR、MATRIX_LR 和 FINAL_LR_FRAC。
```

## Level 2：机制研究与代码注入层

功能：
这是论文的核心模块。它让 LLM 像研究者一样阅读系统代码和实验轨迹，发现搜索瓶颈，然后生成新的搜索机制代码。

触发频率：
每 2 个外层周期执行一次。

Level 2 的 4 轮会话：

1. Explore
   LLM 阅读完整 `runner.py` 和搜索 trace，从组合优化、在线学习、实验设计、贝叶斯优化等相邻领域寻找候选机制。

2. Critique
   LLM 对候选机制做批判，判断哪个最适合当前失败模式，例如重复提案、参数执念、探索不足。

3. Specify
   LLM 写出精确接口，包括类名、构造参数、方法签名，以及和 `runner.py` 的集成点。

4. Generate
   LLM 写出完整、可运行的 Python 代码，并修改 `runner.py` 的调用逻辑。

安全机制：

- 生成代码会先 patch 到 `runner.py`。
- 系统用 `importlib` 动态导入验证。
- 导入成功才激活。
- 导入失败就恢复 pre-patch backup。

论文里生成的机制：

- Tabu Search Manager：维护禁忌列表，阻止系统重复探索最近失败或相近的参数区域。
- Multi-Scale Bandit Proposer：把参数选择当作多臂老虎机，在探索和利用之间平衡。
- Systematic Orthogonal Exploration：强迫系统探索正交参数维度，避免一直盯着同一个方向。
- GP Regressor：尝试过，但因为缺少 `sklearn` 依赖被自动回滚。

关键点：
Level 2 不是简单调参，而是在生成新的“搜索方法”。这是它和 Level 1.5 的本质区别。

## 例子：为什么 Level 2 能发现 TOTAL_BATCH_SIZE 降低

论文里最关键的发现是：在 RTX 5090 + 300 秒训练预算下，降低 `TOTAL_BATCH_SIZE` 反而显著改善 `val_bpb`。

这个发现为什么难？

普通 LLM 的先验可能是：

```text
更大的 batch size 更稳定，吞吐更高，所以应该尝试增大 TOTAL_BATCH_SIZE。
```

纯 Level 1 的行为：

```text
第 1 次：尝试增大 TOTAL_BATCH_SIZE，失败。
后面：继续围绕熟悉参数反复尝试，例如 WEIGHT_DECAY、WINDOW_PATTERN。
结果：没有想到反方向，把 TOTAL_BATCH_SIZE 降低。
```

Level 1.5 的问题：

```text
看到 TOTAL_BATCH_SIZE 增大失败后，可能直接冻结 TOTAL_BATCH_SIZE。
这反而阻止了系统探索“降低 batch size”这个方向。
```

Level 2 的作用：

```text
Tabu Search：
不要重复访问刚失败的方向。

Orthogonal Exploration：
不要只围绕同一批参数转，要强制探索其他维度。

结果：
系统被推着尝试 TOTAL_BATCH_SIZE 的反方向，也就是降低 batch size。
```

为什么降低有效？

在固定 300 秒训练预算下，较小 batch size 可以完成更多 gradient steps。对于这个 50M 参数模型和 RTX 5090 环境，更多更新步数带来的收敛收益超过了大 batch 的吞吐优势。

这就是论文的核心案例：Level 2 打破了 LLM 默认搜索路径里的偏见。

## 实验设计

论文设置了 4 组消融实验：

| 组别 | 激活层级 | 目的 |
|---|---|---|
| A | Level 1 | 纯内层 Autoresearch baseline |
| B | Level 1 + Level 1.5 | 测试策略调节是否有用 |
| C | Level 1 + Level 1.5 + Level 2 | 完整 Bilevel Autoresearch |
| D | Level 1 + Level 2 | 测试没有 Level 1.5 时 Level 2 是否仍有效 |

控制变量：

- 同一个 LLM：DeepSeek deepseek-chat。
- 同一个 GPU 级别：RTX 5090 32GB。
- 每次训练 300 秒。
- 每组 30 次内层迭代。
- 每组 3 个独立重复。
- 主要指标是 `val_bpb`，越低越好。

## 实验结论

- Group A 有稳定但很小的改进。
- Group B 搜索更分散，但平均收益没有明显超过 Group A。
- Group C，也就是完整结构，平均提升约为 Group A 的 5 倍。
- Group D 说明 Level 2 即使没有 Level 1.5，也能带来大幅提升，但波动更大。
- 论文认为 Level 2 是主要收益来源，Level 1.5 主要提升稳定性和上下文质量。

## 模块分工总结

| 模块 | 解决什么问题 | 能改变什么 | 不能改变什么 |
|---|---|---|---|
| Level 1 | 做具体实验 | 参数配置 | 搜索机制 |
| Level 1.5 | 避免局部打转 | 冻结参数、解冻参数、指导语 | proposal 生成逻辑、接受规则 |
| Level 2 | 改进搜索方法本身 | 生成新搜索机制、patch runner | 仍受代码验证、依赖和 prompt 约束 |
| Validate/Revert | 防止坏代码破坏系统 | 激活或回滚机制 | 判断机制是否科学有效 |

## 我自己的理解

这篇论文最值得记住的是：

```text
不要只让 Agent 在一个固定流程里努力。
更强的做法是：让 Agent 观察这个流程哪里低效，然后改流程本身。
```

它对做 Agent 系统有几个启发：

- 一个 Agent 的能力不只取决于模型，还取决于循环结构。
- 如果系统反复失败，不一定是模型不聪明，可能是搜索机制让它只能在局部打转。
- 机制级改动比提示词级改动更有潜力，但也更危险。
- 任何运行时代码注入都必须有验证、回滚、依赖约束和日志审计。

## 局限

- 每组只有 3 个重复，统计强度有限。
- 只在一个 GPT 预训练 benchmark 上测试，泛化性未知。
- 动态代码注入很脆弱，论文也提到曾有 silent fallback 问题。
- Level 2 可以生成外部依赖，例如 `sklearn`，这会带来环境和安全风险。
- Level 2 的探索方向部分受 prompt 引导，是否能真正开放式发现机制仍未充分验证。

## 相关

- [[AI自我迭代研究范式：Autoresearch技术全景与产业洞察]]
- [[Self-Evolving AI Agents Survey]]
- [[HyperAgents Meta-Level Self-Modifiable Agents]]
- [[AutoResearchClaw]]
