# 视频字幕/文字稿样本标注

> 目标：记录可复用的“讲解动作”，而不是搬运完整字幕。时间戳来自公开视频章节、官方 transcript/字幕入口或第三方 transcript 页面；无法确认精确秒数时，使用章节位置。

## 样本总览

| # | 来源 | 主题 | transcript/字幕可用性 | 重点观察 |
| --- | --- | --- | --- | --- |
| 1 | CS50x Week 3 Algorithms | 搜索、排序、复杂度 | 官方页面提供 Transcript/Subtitles | 生活化演示、先笨后巧 |
| 2 | Karpathy micrograd | 反向传播 | 第三方 transcript 有章节 | 从最小代码对象开始 |
| 3 | Karpathy makemore | 语言模型 | 课程页提供视频入口和章节说明 | 连续升级复杂度 |
| 4 | 李宏毅 ML 2021 课程介绍 | 课程地图 | 官方课程页 + 视频入口 | 先给全貌和学习路径 |
| 5 | 李宏毅 Backpropagation | 反向传播 | Bilibili/YouTube 课程视频，配套课件 | 图示先行、中文口语化 |
| 6 | Khan Academy Binary Search | 二分查找 | 图文教程 + 课程视频入口 | 猜数字类比、规模对比 |
| 7 | MIT 6.006 Lecture 1 | 算法思维/峰值查找 | 课程页视频 + notes | 问题模型和算法思维 |
| 8 | Abdul Bari algorithm video sample | 算法手推 | YouTube + 第三方 transcript 样本 | 板书过程、伪代码节奏 |

## 逐段标注

### 1. CS50x Week 3 Algorithms

来源：https://cs50.harvard.edu/x/weeks/3/

- timestamp/位置：开场到 binary search 引入。
- teaching_action：`hook`、`contrast`、`analogy`。
- segment_summary：从搜索问题进入，先让学生看到线性搜索，再用电话簿/分半思想引出 binary search。
- learner_problem：初学者不知道为什么需要“算法复杂度”，生活化演示先制造效率差。
- reusable_pattern：先演低效方法，再演高效方法，最后给算法名字。
- caution：演示必须补充前提：二分查找依赖有序数据。

### 2. Karpathy micrograd

来源：https://www.textpurr.com/transcript/the-spelled-out-intro-to-neural-networks-and-backpropagation-building-micrograd

- timestamp/位置：00:00:25 micrograd overview；00:19:09 starting the core Value object；00:32:10 manual backpropagation。
- teaching_action：`state_naming`、`manual_walkthrough`、`code_mapping`。
- segment_summary：先说明 micrograd 的目标，再创建最小 `Value` 对象，用手动反向传播解释梯度流。
- learner_problem：学生常觉得反向传播是公式黑箱；这里先让每个中间量可打印、可观察。
- reusable_pattern：先手写一个极小系统，再展示框架只是把同样流程自动化。
- caution：代码优先讲法要求学生有基本 Python 能力，否则要先补语法。

### 3. Karpathy makemore

来源：https://karpathy.ai/zero-to-hero.html

- timestamp/位置：makemore 系列课程说明。
- teaching_action：`progressive_complexity`、`checkpoint`。
- segment_summary：从 bigram 字符模型开始，逐步升级到 MLP、BatchNorm、Transformer。
- learner_problem：复杂系统一次讲完会压垮初学者；版本升级让每个新概念都有来处。
- reusable_pattern：每次引入新概念都回答“旧版本哪里不够用”。
- caution：要避免学生只跟着敲代码而不理解每个版本的改进目标。

### 4. 李宏毅 Machine Learning 2021 课程介绍

来源：https://speech.ee.ntu.edu.tw/~hylee/ml/2021-spring.php

- timestamp/位置：课程介绍与要求。
- teaching_action：`map_first`、`scope_setting`。
- segment_summary：先说明课程覆盖内容、学习目标、作业和资源结构。
- learner_problem：初学者面对机器学习容易不知道路线；课程地图先降低迷路感。
- reusable_pattern：复杂课程第一讲先回答“我们会走哪条路、每段路解决什么问题”。
- caution：地图不能太大，必须标出本讲只处理哪一块。

### 5. 李宏毅 Backpropagation

来源：https://www.bilibili.com/video/BV1qy4y1t7LQ/ 与课程页 https://speech.ee.ntu.edu.tw/~hylee/ml/2021-spring.php

- timestamp/位置：选修 Backpropagation 章节。
- teaching_action：`visual_model`、`formalization`、`pitfall`。
- segment_summary：先用图示展示网络和误差传播，再引入链式法则与局部梯度。
- learner_problem：学生容易只背链式法则，不知道每个符号对应图里的哪条边。
- reusable_pattern：公式出现前，先让图上的节点、箭头、误差信号都有中文解释。
- caution：图示讲完后必须回到一个具体数值例子，否则仍然抽象。

### 6. Khan Academy Binary Search

来源：https://www.khanacademy.org/computing/computer-science/algorithms/binary-search/a/binary-search

- timestamp/位置：Binary search article/video lesson。
- teaching_action：`analogy`、`state_naming`、`formalization`。
- segment_summary：用猜数字建立“合理范围”，再过渡到数组搜索和实现细节。
- learner_problem：初学者不知道 `low/high/mid` 为什么存在；“合理范围”先给变量意义。
- reusable_pattern：变量不要从代码里突然出现，要先从问题状态里自然长出来。
- caution：类比必须说明“有序”和“反馈方向”两个前提。

### 7. MIT 6.006 Lecture 1

来源：https://courses.csail.mit.edu/6.006/fall11/notes.shtml

- timestamp/位置：Lecture 1 Algorithmic Thinking, Peak Finding。
- teaching_action：`problem_modeling`、`correctness`、`complexity_reasoning`。
- segment_summary：从具体问题进入算法思维，强调问题定义、算法策略和效率分析。
- learner_problem：学生可能会把算法当成代码技巧；MIT 的组织方式强调先有问题模型。
- reusable_pattern：每个算法都要回答“输入是什么、输出是什么、什么算正确”。
- caution：严谨讲法要配小例子，否则初学者容易觉得抽象。

### 8. Abdul Bari algorithm video sample

来源：https://www.youtube.com/@abdul_bari 与样本 https://glasp.co/youtube/0IAPZzGSbME

- timestamp/位置：视频开头到伪代码/复杂度分析段。
- teaching_action：`manual_walkthrough`、`pseudocode_after_demo`、`complexity_reasoning`。
- segment_summary：先在板书上手推过程，再写伪代码，最后分析复杂度。
- learner_problem：学生直接看伪代码容易不知道每行在干什么；手推先建立过程感。
- reusable_pattern：过程型算法遵循“例子 -> 步骤 -> 伪代码 -> 复杂度”。
- caution：板书式讲法容易缺少真实代码落地，需要补一段代码映射。

## 初步结论

- 视频讲解的核心优势是“过程可见”：老师可以用停顿、重复、手写、擦除、转场帮学生跟上。
- 好的视频不是把文章念出来，而是不断告诉学生当前处在“直觉、手算、规则、代码、复杂度”的哪一层。
- 初学者友好的字幕/文字稿通常会反复出现同一核心句，只是每次绑定到不同载体：生活例子、图、变量、代码、复杂度。

