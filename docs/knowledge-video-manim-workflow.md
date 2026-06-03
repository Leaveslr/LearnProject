# Manim 知识讲解视频快速生成流程

这份流程用于把一个技术知识点或一章学习资料，快速转换成“小白能看懂”的 Manim 知识讲解视频。默认产物包括：讲解脚本、topic JSON、MP4、内嵌字幕、SRT 字幕、抽帧检查图、评估与迭代记录。

## 适用场景

- 单个技术概念：Attention、KV Cache、LoRA、RAG、ReAct Agent。
- 一章知识点批量视频：例如 `llm-knowledge-book/src/01-基础原理`。
- 需要快速预览、评估、迭代、再高清渲染的知识讲解视频。

## 目录约定

```text
.codex/skills/knowledge-video-manim/
  SKILL.md
  references/
  scripts/

manim_knowledge_videos/
  generic_video.py
  render_topic.py
  topics/
  outputs/
  evaluation.md

llm-knowledge-book/outputs/videos/<chapter>/
  README.md
  scripts/
  subtitles/
  topics/
  final-frames/
  评估与迭代记录.md
```

## 核心脚本结构

一个真正让小白学会的视频，要在一个视频里完成完整学习闭环：

```text
先讲概念 -> 再讲例子 -> 再讲例题 -> 最后总结
```

推荐比例：

- 概念：20%-25%。讲这个知识点是什么、解决什么问题、输入输出是什么、在系统里扮演什么角色。
- 例子：45%-55%。用一个具体例子把概念跑通，展示每一步细节。
- 例题：20%-30%。换一个相似小题，让用户当场应用并解释原因。
- 总结：5%-10%。只留下 2-3 条可迁移判断规则。

概念负责“知道它是什么”，例子负责“带着走”，例题负责“自己走”，总结负责“带得走”。四者都完成，用户才算真正懂了。

### 标准脚本骨架

| 阶段 | 目标 | 典型问题 |
| --- | --- | --- |
| 1. Hook | 让用户知道为什么要学 | 这个概念到底解决什么痛点？ |
| 2. 概念地图 | 给地图，不堆术语 | 它是什么、解决什么问题、输入输出是什么、扮演什么角色？ |
| 3. 讲例子 | 固定心智锚点 | 我们用哪个例子把概念跑通？ |
| 4. 机制拆解 | 一步一步走例子 | 这个例子里的每一步发生了什么？ |
| 5. 关键细节 | 补真正会卡住的地方 | 公式、边界、实现细节分别是什么意思？ |
| 6. 反事实/对比 | 解释为什么这样做 | 如果不这样做，会错在哪里？ |
| 7. 讲例题 | 验证是否真懂 | 换一个小题，用户能不能自己应用？ |
| 8. 总结 | 收束成可迁移判断规则 | 用户离开视频后遇到新题能怎么判断？ |

### 例题设计

例题必须检查理解，而不是背诵。合格例题通常长这样：

- 换一个输入，让用户找出正确 token 的概率。
- 改变一个数值，让用户判断 loss 会升还是降。
- 改一个 mask 或模块，让用户判断训练目标会不会变。
- 给一个指标结果，让用户判断它能说明什么、不能说明什么。

如果用户只能复述例子，不能完成例题，说明视频还只是“讲过了”，没有“学会”。

## 一次生成的执行步骤

### 1. 拆知识点

先读原始资料，按“一个视频只解决一个核心问题”拆分。每个视频必须覆盖：

- hook：为什么要学它
- naive problem：新手会卡在哪里
- concept role：它是什么、解决什么问题、在系统里负责什么
- core mechanism：核心机制
- concrete walk-through：一个具体例子
- transfer exercise：一个相似但不完全一样的例题
- boundary/caveat：边界、误区、易混点
- summary：可迁移判断规则

批量章节建议一个 Markdown 小节或一个独立主题对应一个视频，避免单条视频塞太多概念。

拆完后必须确定一个贯穿例子。没有贯穿例子的脚本，默认不进入渲染阶段。
如果概念段不能用一句话说清“它不是/它是/它负责”，也默认不进入渲染阶段。

### 2. 写 topic JSON

在 `manim_knowledge_videos/topics/` 新建主题文件。每段控制在 6-9 秒，字幕一口气能读完。

topic JSON 建议按这个顺序组织：

1. 标题问题：一句话说明本视频解决什么困惑。
2. 概念地图：讲它是什么、解决什么问题、输入输出、系统角色。
3. 例子起点：把用户带入一个具体输入。
4. 机制链路：用同一个例子走完关键步骤。
5. 细节放大：公式、概率、缓存、mask、权重等难点逐个解释。
6. 前后对比：展示训练前后、优化前后、错误/正确做法差异。
7. 例题讲解：换一个相似小题，让用户应用刚才的机制。
8. 总结：2-3 条可迁移判断规则。

最常用 visual 类型：

- `title`：开场问题
- `compare`：对比概念
- `pipeline`：流程链路
- `trace`：逐项解释
- `formula`：公式拆解
- `bars`：概率或数值对比
- `loop`：循环工作流
- `summary`：三点总结，适合短句

视觉选择补充：

- 总结句较长时，优先用 `trace`，左侧放“概念/例子/例题/规则”标签，右侧放短解释。
- 不要把短文本强行拉宽；文本组件应优先使用 `max_width`，避免短句被放大到失控。
- 如果一页有三条以上长解释，先拆段，不要依赖缩放硬塞。

写完后检查 JSON：

```bash
python3 -m json.tool manim_knowledge_videos/topics/<topic>.json >/dev/null
```

### 3. 低清预览渲染

使用本地 Manim 环境：

```bash
. /Users/lr/.cache/codex-manim-venv/bin/activate
cd /Users/lr/Documents/Codex/LearnProject/manim_knowledge_videos
python render_topic.py topics/<topic>.json --quality=-ql --quality-dir 480p15
```

批量渲染：

```bash
. /Users/lr/.cache/codex-manim-venv/bin/activate
cd /Users/lr/Documents/Codex/LearnProject/manim_knowledge_videos
for topic in topics/ch01_*.json; do
  python render_topic.py "$topic" --quality=-ql --quality-dir 480p15
done
```

### 4. 抽帧检查

预览版必须抽帧检查，尤其要看段落边界。常见问题是：字幕还在，但主画面已经淡出，学习密度下降。

```bash
. /Users/lr/.cache/codex-manim-venv/bin/activate
cd /Users/lr/Documents/Codex/LearnProject/manim_knowledge_videos

slug=<topic-slug>
mkdir -p outputs/$slug/frames_v1
for t in 00:00:05 00:00:24 00:00:40 00:00:56 00:01:10; do
  name=$(printf '%s' "$t" | tr ':' '-')
  ffmpeg -y -ss "$t" -i outputs/$slug/${slug}_480p15.mp4 \
    -frames:v 1 outputs/$slug/frames_v1/frame_$name.png >/dev/null 2>&1
done
```

检查维度：

- 画面主体是否清楚
- 字幕是否遮挡内容
- 一屏是否超过 3 个核心对象
- 公式是否已经被例子铺垫
- 新手是否知道“为什么”和“怎么用”
- 是否有边界条件和常见误区
- 概念段是否能让用户说出“它是什么”
- 例题是否真的要求迁移，而不是复述
- 总结页在动画进入时是否有文字重叠，不只看最后稳定帧

抽帧至少覆盖四类画面：

1. 概念入口帧
2. 贯穿例子关键帧
3. 例题提问和揭答案帧
4. 总结稳定帧，以及总结动画进入后的早期帧

### 5. 评估并迭代

按 100 分评估：

- 概念清晰 20 分：用户知道它是什么、解决什么问题、输入输出是什么
- 例子讲透 20 分：同一个例子能走完整条机制链
- 准确完整 20 分：机制、公式、边界不缺
- 例题迁移 20 分：用户能做对相似小题并解释原因
- 视觉节奏 10 分：每屏只做一个认知动作
- 工程产物 10 分：MP4、SRT、脚本、抽帧、评估齐全

评估时用四个通过问题：

```text
它是什么？
细节怎么发生？
这个例子为什么这样跑？
换一个相似题，我能不能判断？
```

低于 90 分必须迭代。常见补强方式：

- 把概念入口改成“不是 X，而是 Y，它负责 Z”
- 增加“训练 vs 推理”“token embedding vs retrieval embedding”这类易混边界
- 把抽象公式拆成 2-3 张卡片解释
- 加一个数字例子，让用户能感知大小关系
- 加一个反事实：如果不这么做，会错在哪里
- 加一道同构例题，验证用户是否能迁移应用
- 缩短过场淡出，让主画面停留更久
- 把过长字幕拆成更短句
- 把长总结页改成 `trace` 三行判断规则
- 修复通用模板里的文字缩放问题，而不是只改单条视频

### 6. 高清最终渲染

```bash
. /Users/lr/.cache/codex-manim-venv/bin/activate
cd /Users/lr/Documents/Codex/LearnProject/manim_knowledge_videos
python render_topic.py topics/<topic>.json --quality=-qm --quality-dir 720p30
```

批量渲染：

```bash
. /Users/lr/.cache/codex-manim-venv/bin/activate
cd /Users/lr/Documents/Codex/LearnProject/manim_knowledge_videos
for topic in topics/ch01_*.json; do
  python render_topic.py "$topic" --quality=-qm --quality-dir 720p30
done
```

### 7. 校验成品

确认每个 MP4 都有视频流、音频流、720p、30fps：

```bash
. /Users/lr/.cache/codex-manim-venv/bin/activate
for f in llm-knowledge-book/outputs/videos/<chapter>/*.mp4; do
  echo "$f"
  ffmpeg -i "$f" 2>&1 | rg 'Duration|Stream'
done
```

### 8. 整理交付目录

把最终资料整理到章节目录：

```text
llm-knowledge-book/outputs/videos/<chapter>/
  01-主题名.mp4
  README.md
  scripts/01-主题名.md
  subtitles/01-主题名.srt
  topics/topic_slug.json
  final-frames/*.png
  评估与迭代记录.md
```

视频文件可以保留在本地，但默认不提交到 Git。提交远端时只提交非视频资料：

- skill
- 生成脚本
- topic JSON
- 讲解脚本
- SRT 字幕
- 评估文档
- 少量最终抽帧证据

不要提交：

- `*.mp4`
- `*.wav`
- `*.aiff`
- Manim `media/`
- `__pycache__/`
- `.DS_Store`

## 快速复用提示词

```text
使用 knowledge-video-manim 流程，把 <资料路径或知识点> 转成小白能懂的 Manim 知识讲解视频。
要求：
1. 先拆讲解脚本和 topic JSON
2. 低清预览渲染并抽帧评估
3. 至少迭代一轮，补齐边界和易混点
4. 高清渲染 720p30
5. 输出 MP4、SRT、脚本、topic、评估记录
6. 非视频资产提交远端，视频本地保留
中间不用询问，持续迭代到 90 分以上。
```

## 故障处理

- 如果 `python` 不存在，用 `python3`。
- 如果 Manim 找不到依赖，先激活 `/Users/lr/.cache/codex-manim-venv`。
- 如果 `--quality -ql` 报参数错误，使用 `--quality=-ql`。
- 如果画面出现空窗，优先调整 `generic_video.py` 的过场时间和 hold 逻辑。
- 如果中文语音不生成，确认 macOS `say -v Tingting` 可用。
- 如果仓库出现大量渲染缓存，先检查 `.gitignore`，再只手动 `git add` 非视频资产。

## 提交前检查

```bash
git diff --cached --check
git diff --cached --name-only | rg '\\.(mp4|wav|aiff|pyc)$|__pycache__|/media/|DS_Store' || true
git status --short
```

确认没有视频和缓存后再提交：

```bash
git commit -m "Add knowledge video workflow documentation"
git push origin main
```
