# Karpathy 讲解方式分析

## 样本

- Neural Networks: Zero to Hero：https://karpathy.ai/zero-to-hero.html
- micrograd transcript：https://www.textpurr.com/transcript/the-spelled-out-intro-to-neural-networks-and-backpropagation-building-micrograd
- Hacker's Guide to Neural Networks：https://karpathy.github.io/neuralnets/

## 核心风格

Karpathy 的强项不是把概念压缩成定义，而是把概念还原成可以运行、可以调试、可以观察的最小系统。他常用的路径是：

`最小代码对象 -> 手动计算 -> 可视化中间状态 -> 自动化封装 -> 和真实框架对照`

## 讲解动作

- 先造一个玩具世界：例如一个 `Value` 对象、一小段表达式、一个字符级语言模型。
- 让学习者看到中间状态：数值、梯度、计算图、loss、采样结果。
- 先手动做，再抽象成函数或类。
- 每次封装后马上验证结果，防止抽象漂浮。
- 从自制小系统过渡到 PyTorch，让学生知道框架并不神秘。

## 对初学者友好的地方

- “from scratch in code”降低了抽象门槛：学习者可以运行、打印、改动。
- “spelled-out”意味着不跳步，尤其适合反向传播这种容易被公式吓退的主题。
- 复杂概念被拆成连续版本：micrograd -> makemore -> MLP -> batchnorm -> transformer。

## 可复用原则

- 讲抽象系统时，先设计一个最小可运行模型。
- 每个新概念都要接在一个已有代码缺陷或需求后面。
- 公式可以晚一点出现，但中间量必须早一点出现。
- 学生应当能回答：“这行代码对应概念图里的哪一块？”

## 示例句式

- “我们先不使用框架，手动实现一个只够说明问题的小版本。”
- “现在这个版本能跑，但它有一个明显限制：……”
- “先把中间结果打印出来，看它到底在流动什么。”
- “PyTorch 做的事情没有魔法，它只是把我们刚才手写的流程工程化了。”

