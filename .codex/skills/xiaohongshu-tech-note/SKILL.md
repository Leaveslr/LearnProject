---
name: xiaohongshu-tech-note
description: Use when turning technical learning notes, LLM knowledge-book chapters, interview topics, or engineering concepts into Xiaohongshu/RedNote 图文笔记, including titles, cover copy,正文,配图建议, tags, and publish-ready Markdown drafts.
---

# Xiaohongshu Tech Note

## Overview

Use this skill to convert technical notes into 小红书图文内容 for AI/LLM learners and interview-prep readers. Optimize for clarity, collection value, and credible technical explanation, not hollow viral copy.

## Required Inputs

Before writing, identify or infer:

- Knowledge point: one specific topic, not an entire domain.
- Audience: default to LLM beginner preparing for AI algorithm/engineering interviews.
- Source note: prefer `llm-knowledge-book/src/**`.
- Output path: default to `llm-knowledge-book/outputs/xiaohongshu/`.

If the user gives a broad topic like “Transformer 详解”, narrow it into one note angle unless they explicitly want a long-form series overview.

## Workflow

1. Read the relevant source note from `llm-knowledge-book/src`.
2. Read project templates only when needed:
   - `llm-knowledge-book/templates/小红书图文笔记模板.md`
   - `llm-knowledge-book/src/00-学习路线/02-学习笔记到内容创作工作流.md`
3. If writing style or structure is unclear, read `references/writing-patterns.md`.
4. Draft in this order:
   - 5-8 title candidates
   - cover copy, 12-20 Chinese characters
   - opening hook, 2-3 short lines
   - body with 4-6 compact sections
   - one example or analogy
   - common misunderstanding
   - interview answer card
   - image/card suggestions
   - tags
5. Save the draft as Markdown when the user asks to write or persist the note.

## Writing Rules

- Make one note about one clear point.
- Start from a pain point or misconception.
- Prefer “一句话结论 -> 直觉 -> 机制 -> 误区 -> 面试回答”.
- Use short paragraphs and scannable bullets.
- Keep technical claims accurate; do not exaggerate model behavior.
- Use formulas sparingly and always explain them in plain Chinese.
- Avoid fake certainty, clickbait, and generic motivational filler.
- End with a natural next-note pointer.

## Output Format

Use this Markdown structure:

```markdown
# 小红书图文笔记：<topic>

## 标题候选

## 推荐标题

## 封面文案

## 正文

## 配图建议

## 标签

## 下一篇选题
```

For technical interview topics, include:

```markdown
## 面试回答卡
```

