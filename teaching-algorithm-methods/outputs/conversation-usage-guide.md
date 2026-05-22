# 对话框使用指南：如何加载讲解技巧

## 使用目标

当你后续要讲解一个知识点时，可以直接在对话框里要求助手加载本目录中的方法论文档，然后按固定流程帮你拆解、备课、生成讲解稿或检查讲解质量。

推荐把本目录当作“讲解方法库”，每次按任务需要加载最少文件。

## 最推荐加载顺序

### 1. 快速备课

适合：你已经知道要讲什么，只想快速得到讲解结构。

加载文件：

- `outputs/quick-reference.md`
- `abstracted-methods/script-template.md`
- `abstracted-methods/checklist.md`

可复制提示词：

```text
请基于 /Users/lr/Documents/Codex/LearnProject/teaching-algorithm-methods 里的讲解方法论，
重点加载 outputs/quick-reference.md、abstracted-methods/script-template.md、abstracted-methods/checklist.md。

我要讲解的知识点是：____
目标受众是：____
请帮我生成一份适合讲解的结构化大纲，必须包含：
1. 问题场景
2. 朴素做法
3. 核心直觉
4. 手算小例子
5. 变量/状态解释
6. 代码或伪代码
7. 正确性/复杂度
8. 易错点和反例
9. 迁移练习
```

## 2. 深度备课

适合：你要把一个知识点讲得非常清楚，甚至做成课程内容。

加载文件：

- `outputs/methodology-handbook.md`
- `outputs/expert-review-and-optimization.md`
- `abstracted-methods/knowledge-breakdown-framework.md`
- `abstracted-methods/script-template.md`
- 相关验证案例，例如 `validation-cases/sliding-window-walkthrough.md`

可复制提示词：

```text
请作为知识讲解专家，加载并遵循：
/Users/lr/Documents/Codex/LearnProject/teaching-algorithm-methods/outputs/methodology-handbook.md
/Users/lr/Documents/Codex/LearnProject/teaching-algorithm-methods/outputs/expert-review-and-optimization.md
/Users/lr/Documents/Codex/LearnProject/teaching-algorithm-methods/abstracted-methods/knowledge-breakdown-framework.md
/Users/lr/Documents/Codex/LearnProject/teaching-algorithm-methods/abstracted-methods/script-template.md

我要讲解的知识点是：____
受众水平是：____
讲解时长是：____
希望风格是：____

请先拆解这个知识点的认知难点，再生成完整讲解稿。
讲解稿必须体现：
- 先问题后概念
- 先直觉后术语
- 先手算后代码
- 有诊断问题
- 有学生卡住时的降阶策略
- 有反例和适用边界
- 有同型练习、变式练习和不能用的判断题
```

## 3. 检查已有讲稿

适合：你已经写了一版讲解稿，想检查哪里不清楚。

加载文件：

- `outputs/expert-review-and-optimization.md`
- `abstracted-methods/checklist.md`
- `abstracted-methods/video-transcript-coding-guide.md`

可复制提示词：

```text
请加载 /Users/lr/Documents/Codex/LearnProject/teaching-algorithm-methods 中的讲解质量检查方法，
重点参考 outputs/expert-review-and-optimization.md 和 abstracted-methods/checklist.md。

下面是我的讲解稿：
____

请从知识讲解专家角度评估：
1. 学习者是否知道为什么要学
2. 是否有清晰直觉模型
3. 是否有可手算的小例子
4. 代码/公式是否和直觉对齐
5. 是否解释了适用前提和反例
6. 是否有诊断问题和降阶策略
7. 是否有练习帮助迁移

请给出具体修改建议，并重写一版更清楚的讲解结构。
```

## 4. 模仿名师风格

适合：你想让讲解更像某位老师的风格。

加载文件：

- `analysis-notes/karpathy.md`
- `analysis-notes/hung-yi-lee.md`
- `analysis-notes/mit-cs50-khan-abdul.md`
- `raw-materials/video-transcript-samples.md`

可复制提示词：

```text
请加载 /Users/lr/Documents/Codex/LearnProject/teaching-algorithm-methods 的名师分析笔记：
analysis-notes/karpathy.md
analysis-notes/hung-yi-lee.md
analysis-notes/mit-cs50-khan-abdul.md
raw-materials/video-transcript-samples.md

我要讲解的知识点是：____
请分别用以下三种风格给我设计讲解路径：
1. Karpathy 风格：从最小可运行代码/系统开始，逐层复杂化
2. 李宏毅风格：先给全貌地图，用口语问题和图示建立直觉
3. CS50/Khan 风格：用生活化问题和小例子引入，再过渡到算法

最后请融合成一版最适合编程初学者的讲解方案。
```

## 5. 一句话快捷调用

如果不想写太多，可以直接用：

```text
请加载 /Users/lr/Documents/Codex/LearnProject/teaching-algorithm-methods 里的讲解方法论，
按“问题场景 -> 已有经验 -> 直觉模型 -> 手算 -> 形式化 -> 代码 -> 正确性/复杂度 -> 易错点/反例 -> 迁移练习”的流程，
帮我讲清楚这个知识点：____
受众是：____
```

## 6. 建议补充的信息

为了让生成结果更准，最好在对话里补充：

- 知识点名称：例如二分查找、滑动窗口、Transformer attention。
- 受众水平：零基础、会基础语法、刷题入门、工程师转 AI。
- 输出形式：大纲、讲解稿、课件结构、视频脚本、练习题。
- 讲解时长：5 分钟、15 分钟、45 分钟。
- 是否需要代码：不需要、伪代码、Python、JavaScript、C++。
- 风格偏好：Karpathy、李宏毅、CS50、板书式、图文教程式。

## 7. 推荐默认参数

如果没有额外说明，默认使用：

- 受众：编程初学者。
- 输出：结构化讲解稿。
- 代码：Python 伪代码优先。
- 风格：Khan Academy 的初学者路径 + Karpathy 的最小可运行系统 + 李宏毅的全貌地图。
- 必须包含：反例、诊断问题、降阶策略和迁移练习。

