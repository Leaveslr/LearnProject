# OneTrans 技术分享：用一个 Transformer 统一特征交互与序列建模

## 论文信息

- 论文：OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender
- 作者：Zhaoqi Zhang, Haolei Pei, Jun Guo, Tianyu Wang, Yufei Feng, Hui Sun, Shaowei Liu, Aixin Sun
- 机构：ByteDance, Nanyang Technological University
- 版本：arXiv:2510.26104v3，2026-02-02
- 会议：The Web Conference 2026，camera-ready forthcoming
- 论文链接：https://arxiv.org/abs/2510.26104
- PDF：../papaer/OneTrans_Unified_Feature_Interaction_and_Sequence_Modeling_with_One_Transformer_in_Industrial_Recommender.pdf

## 一句话总结

OneTrans 把推荐排序模型里原本分开的“用户行为序列建模”和“非序列特征交互”合并到同一个因果 Transformer backbone 中，用统一 token 序列、混合参数化、金字塔式 token 收缩和跨请求 KV Cache，让推荐排序模型可以像 LLM 一样整体扩展，并在字节工业场景线上 A/B 中带来显著收益。

## 背景：为什么需要 OneTrans

工业推荐排序常见结构是 DLRM 风格的级联排序模型。召回先从海量候选中取出几百个 item，排序模型再根据用户、候选 item、上下文和历史行为序列预测 CTR、CVR 等目标。

传统排序模型通常有两条独立演进路线：

1. 序列建模模块：例如 DIN、Transformer、LONGER，用用户历史行为序列理解兴趣。
2. 特征交互模块：例如 DCNv2、Wukong、HiFormer、RankMixer，用非序列特征做高阶交叉。

这种“先压缩序列，再和非序列特征拼接交互”的结构有两个问题：

- 信息流被截断：用户静态特征、候选 item 特征、上下文特征很难在早期反向影响序列表示。
- 系统执行割裂：序列模块和交互模块分别设计、分别扩展、分别优化，不利于复用 Transformer 生态里的 FlashAttention、KV Cache、混合精度等成熟优化。

OneTrans 的核心动机是：既然序列建模和特征交互本质上都是 token 间的信息交换，为什么不用一个统一 Transformer 来做？

## 方法总览

OneTrans 的整体链路可以拆成四步：

1. 统一 tokenization

   将输入拆成两类 token：

   - S-tokens：用户多行为序列 token，例如点击、加购、购买等历史行为。
   - NS-tokens：非序列 token，例如用户画像、item 特征、上下文特征。

   最终拼成一个序列：

   ```text
   [S-tokens ; NS-tokens]
   ```

2. 统一因果 Transformer

   使用 causal mask，让后面的 token 可以看前面的 token。论文将 S-tokens 放在前面，NS-tokens 放在后面，因此 NS-tokens 可以聚合用户完整行为历史，最后由 NS-token 表示进入多任务 tower。

3. 混合参数化

   推荐系统的 token 不像文本 token 那样同质。OneTrans 采用混合参数化：

   - 所有 S-tokens 共享一套 Q/K/V 和 FFN 参数，因为它们都是行为序列事件。
   - 每个 NS-token 使用 token-specific 的 Q/K/V 和 FFN 参数，因为用户、item、上下文等非序列特征语义差异很大。

4. 金字塔堆叠

   深层模型不保留所有序列 query，只保留尾部一小部分 token 发起查询，但 K/V 仍来自完整上下文。随着层数加深，序列长度逐步收缩，最终压缩到与 NS-token 数量匹配。

   这相当于把长行为历史逐层蒸馏进更少的 token 中，降低计算和显存，又保留足够的历史信息。

## 关键设计细节

### 1. 非序列特征 Tokenizer

论文比较了两种非序列特征 token 化方式：

- Group-wise Tokenizer：人工按语义分组，每组过一个 MLP，类似 RankMixer。
- Auto-Split Tokenizer：所有非序列特征先拼接，经一个 MLP 投影后自动切分成多个 token。

实验中 Auto-Split 更好。一个重要原因是它减少了手工分组依赖，也降低了多组 MLP 带来的 kernel launch 开销。

### 2. 序列特征 Tokenizer

用户可能有多种行为序列，每个事件由 item id 及 side information 组成。OneTrans 先用序列对应的 MLP 将事件投影到统一维度，再合并多行为序列。

合并方式有两种：

- Timestamp-aware：按时间顺序混排所有行为，并加行为类型标识。
- Timestamp-agnostic：按行为意图强度拼接，例如购买、加购、点击，并用可学习的 [SEP] 分隔。

当时间戳可用时，Timestamp-aware 效果更好；如果无法按时间混排，[SEP] token 对区分多行为序列有帮助。

### 3. Causal Attention 而不是 Full Attention

消融显示 full attention 与 causal attention 指标接近，但 full attention 不利于 KV Cache。OneTrans 选择 causal attention 的重点不是单纯追求离线指标，而是为了让训练和推理都能继承 LLM 里的高效缓存与注意力优化。

### 4. 跨候选与跨请求 KV Cache

工业推荐的一个特点是：同一个请求里有很多候选 item，用户行为序列相同，候选 item 相关的 NS-token 不同。

OneTrans 利用这个结构做两阶段计算：

- Stage I：每个请求只计算一次 S-side，并缓存 K/V。
- Stage II：每个候选只计算自己的 NS-token，并对缓存的 S-side K/V 做 cross attention。

进一步地，用户行为序列通常是 append-only。跨请求时，可以复用上一请求缓存，只计算新增行为的 K/V，把序列侧计算从 O(L) 降到 O(delta L)。

## 实验结论

### 离线效果

论文在 29.1B impressions、27.9M 用户、10.2M item 的工业数据集上评估 CTR/CVR 的 AUC 和 UAUC。

相对 DCNv2 + DIN 基线：

- RankMixer + Transformer：CTR UAUC +0.90%，CVR UAUC +0.75%。
- OneTransS：CTR UAUC +1.77%，CVR UAUC +1.66%。
- OneTransL：CTR UAUC +2.79%，CVR UAUC +3.23%。

这说明统一建模不是简单换 backbone，而是明显超过“强特征交互模块 + 强序列模块”的组合。

### 系统效率

OneTransL 有 330M dense 参数，训练 TFLOPs 是 DCNv2+DIN 的 100 倍以上，但在线 p99 latency 反而略低：

- DCNv2+DIN p99：13.6 ms
- OneTransL p99：13.2 ms

关键原因是模型结构统一后，可以系统性使用：

- Pyramid stack
- Cross-request KV caching
- FlashAttention-2
- 混合精度与 recomputation

### Scaling Law

论文分别沿 length、depth、width 扩展 OneTrans。结论是：

- 增加行为序列长度收益最大，因为引入了更多用户历史证据。
- depth 和 width 都有收益，但 depth 通常更高效。
- OneTrans 的 compute-performance 曲线比 RankMixer + Transformer 更陡，说明统一 backbone 更适合继续扩展。

### 线上 A/B

对比线上控制组 RankMixer + Transformer，OneTransL 带来：

Feeds 场景：

- click/u：+7.737%
- order/u：+4.351%
- gmv/u：+5.685%
- p99 latency：-3.91%

Mall 场景：

- click/u：+5.143%
- order/u：+2.577%
- gmv/u：+3.670%
- p99 latency：-3.26%

论文还提到 Active Days +0.7478%，冷启动商品 order/u +13.59%，说明统一建模可能改善泛化能力和冷启动表现。

## 技术分享讲稿提纲

### 开场：推荐排序模型的两条增长曲线

可以先讲工业排序模型的两个长期方向：

- 一条线做特征交互，从 Wide & Deep、DeepFM、DCN 到 Wukong、RankMixer。
- 一条线做行为序列，从 DIN、BST 到 LONGER。

问题是这两条线越做越强，但结构上仍然分离。OneTrans 的问题意识是：能不能把这两件事统一为“token 之间的信息交换”？

### 第二部分：OneTrans 的结构

重点讲图 2 的三个模块：

- Tokenizer：S-token 与 NS-token 统一成一个序列。
- OneTrans Block：pre-norm causal Transformer，加 mixed attention 与 mixed FFN。
- Pyramid Stack：逐层减少序列 query，把长历史压缩进尾部 token 和 NS-token。

这里建议强调：OneTrans 不是把 LLM 直接搬进推荐，而是保留 Transformer 统一计算图，同时针对推荐 token 异质性做了 mixed parameterization。

### 第三部分：为什么它能上线

很多大模型推荐论文的问题是离线好，线上慢。OneTrans 的工程亮点是它从结构上服务于缓存：

- 同一请求内，几百个候选共享用户行为序列。
- 跨请求时，用户行为通常只追加少量新事件。
- Causal mask 让 S-side K/V 可以自然缓存。

所以 OneTrans 的线上故事不是“模型更大但硬扛”，而是“统一 backbone 让缓存、FlashAttention 和混合精度都变成系统级收益”。

### 第四部分：结果怎么解读

分享时可以把实验结果分成三层：

1. 离线：OneTransS 和 OneTransL 均明显超过强 baseline。
2. 效率：OneTransL 参数和 FLOPs 大很多，但 p99 latency 与小模型相当甚至略低。
3. 线上：GMV、order、click 同涨，latency 下降，说明收益不是只停留在离线指标。

### 第五部分：可以追问的问题

- NS-token 的 token-specific 参数会不会在特征数量变大时造成参数膨胀？
- Auto-Split Tokenizer 是否会损失可解释性？
- KV Cache 对用户行为更新频率、候选生成方式、在线特征实时性有什么要求？
- Pyramid schedule 是 heuristic，是否可以学习化或自动搜索？
- OneTrans 更适合粗排、精排，还是多阶段排序中的统一 backbone？

## 对我们做推荐系统的启发

1. 统一架构可能比单点模块扩展更重要。

   当序列模块和特征交互模块分开扩展时，二者之间的信息交换会成为瓶颈。OneTrans 的优势不是某个局部模块更强，而是让推荐排序的主要信息交互都发生在同一计算图内。

2. 推荐模型 scaling 需要模型和系统一起设计。

   OneTrans 的离线增益依赖大 backbone，但线上可用性依赖 causal attention、KV Cache、pyramid stack 和 FlashAttention。如果只学模型结构，不学系统优化，很难复现论文里的部署效果。

3. 推荐 token 与文本 token 不同。

   文本 token 大体同质，可以共享参数；推荐系统里用户、item、上下文、序列事件的语义差异很强。mixed parameterization 是一个很实用的折中：序列 token 共享，非序列 token 特化。

4. 长行为序列仍然是最强的 scaling 方向之一。

   论文的 scaling 实验显示，增加 length 收益最大。这与工业直觉一致：更多真实行为历史通常比单纯加宽 MLP 更有信息量。

## 局限与注意事项

- 论文主要基于字节内部工业数据，公开数据复现难度较高。
- 线上收益依赖强工程基础设施，包括连续请求缓存、GPU serving、混合精度和高效 attention kernel。
- NS-token 的自动切分虽然效果好，但可解释性弱于人工分组。
- Pyramid schedule 使用启发式规则，是否对不同业务和序列长度稳定仍需要验证。
- 论文关注排序阶段；在召回、粗排或生成式推荐框架中的迁移还需要进一步实验。

## 适合放在分享结尾的一页

OneTrans 的核心价值可以概括为三句话：

1. 统一建模：把序列建模和特征交互都变成一个 Transformer token 序列里的信息交换。
2. 推荐适配：用 mixed parameterization 处理推荐 token 的异质性。
3. 工程可用：用 causal attention、pyramid stack 和 KV Cache 把大模型推荐带到可上线的延迟范围。

如果用一句话收束：OneTrans 是把推荐排序模型从“模块拼装式扩展”推向“统一 backbone 式扩展”的一次工业级尝试。
