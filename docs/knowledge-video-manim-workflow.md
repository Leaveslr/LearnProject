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

## 一次生成的执行步骤

### 1. 拆知识点

先读原始资料，按“一个视频只解决一个核心问题”拆分。每个视频必须覆盖：

- hook：为什么要学它
- naive problem：新手会卡在哪里
- core mechanism：核心机制
- concrete walk-through：一个具体例子
- boundary/caveat：边界、误区、易混点
- summary：三句话总结

批量章节建议一个 Markdown 小节或一个独立主题对应一个视频，避免单条视频塞太多概念。

### 2. 写 topic JSON

在 `manim_knowledge_videos/topics/` 新建主题文件。每段控制在 6-9 秒，字幕一口气能读完。

最常用 visual 类型：

- `title`：开场问题
- `compare`：对比概念
- `pipeline`：流程链路
- `trace`：逐项解释
- `formula`：公式拆解
- `bars`：概率或数值对比
- `loop`：循环工作流
- `summary`：三点总结

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

### 5. 评估并迭代

按 100 分评估：

- 讲解逻辑 25 分：问题先行，术语后置
- 准确完整 25 分：机制、公式、边界不缺
- 小白可懂 20 分：例子和类比足够具体
- 视觉节奏 15 分：每屏只做一个认知动作
- 工程产物 15 分：MP4、SRT、脚本、抽帧、评估齐全

低于 90 分必须迭代。常见补强方式：

- 增加“训练 vs 推理”“token embedding vs retrieval embedding”这类易混边界
- 把抽象公式拆成 2-3 张卡片解释
- 缩短过场淡出，让主画面停留更久
- 把过长字幕拆成更短句

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
