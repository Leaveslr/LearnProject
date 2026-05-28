# 03-Embedding与向量相似度 视频讲解脚本

标题：Embedding 与向量相似度

| 段落 | 时长 | 字幕/旁白 | 画面类型 |
| --- | ---: | --- | --- |
| 1 | 6.5s | 神经网络不能直接处理文字。Embedding 的作用，就是把离散 token 变成可以计算的向量。 | title |
| 2 | 8.0s | 只给 token 编号是不够的。猫等于 12、狗等于 983，数字大小本身没有语义。 | compare |
| 3 | 8.0s | Embedding 表本质是一个大矩阵。输入 token id 后，模型从矩阵里取出对应那一行。 | pipeline |
| 4 | 8.0s | 训练得好时，语义相近的 token 会在向量空间里更接近，比如猫和狗通常比猫和飞机更接近。 | tokens |
| 5 | 8.0s | 要区分 token embedding 和上下文表示。前者是初始向量，后者是经过 Transformer 后的动态表示。 | compare |
| 6 | 8.0s | 同一个“苹果”，在“吃苹果”和“苹果公司股票”里，初始 embedding 可以相同，但上下文表示会不同。 | trace |
| 7 | 8.0s | 向量相似度常用点积或余弦相似度。余弦相似度关心两个向量方向是否接近。 | formula |
| 8 | 8.0s | RAG 里，Embedding 负责先找资料。如果 query 和文档没有被映射到相近位置，后面生成再强也拿不到证据。 | pipeline |
| 9 | 8.0s | 也要注意：RAG 用的检索 embedding，和生成模型内部的 token embedding，不一定是同一个模型或同一套向量空间。 | compare |
| 10 | 8.0s | 记住三句话：Embedding 是可训练查表；上下文表示会动态变化；向量相似不等于答案一定正确。 | summary |
