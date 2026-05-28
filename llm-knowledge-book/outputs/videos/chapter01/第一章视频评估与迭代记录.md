# Chapter 01 Knowledge Video Evaluation

## Scope

Converted `llm-knowledge-book/src/01-基础原理` into five beginner explainer videos:

1. 机器学习与深度学习基础
2. 损失函数与交叉熵
3. Embedding 与向量相似度
4. AdamW 与学习率调度
5. 归一化、残差与激活函数

## V1 Preview Review

| Video | Score | Strength | Main Gap |
| --- | ---: | --- | --- |
| 机器学习与深度学习基础 | 88 | Gives a good top-level map: probability, representation, optimization | Needed clearer distinction between training and inference |
| 损失函数与交叉熵 | 90 | Clear loss intuition, formula, PPL caveat | Needed SFT loss-mask boundary |
| Embedding 与向量相似度 | 89 | Separates token id, embedding, contextual representation, RAG retrieval | Needed distinction between LLM token embedding and retrieval embedding |
| AdamW 与学习率调度 | 88 | Explains gradient, lr, AdamW, warmup, stability tools | Needed practical fine-tuning failure checklist beyond lr |
| 归一化、残差与激活函数 | 90 | Covers block structure, residual, LayerNorm, Pre-Norm, activation, SwiGLU | Needed more explicit architecture-choice caveat |

## Frame And Rhythm Review

- Preview videos all contain 16:9 video, audio, and subtitle tracks.
- Extracted frames showed some frames near transitions with only title/subtitle visible.
- Root cause: stage fade-out was long enough that sampled boundary frames could look visually empty.
- Template iteration shortened scene fade-out and added a minimum hold helper so the main visual remains visible for most of each narration segment.

## Iteration Applied

- Added a training-vs-inference boundary segment to the ML/DL basics video.
- Added an SFT loss-mask segment to cross entropy.
- Added an LLM token embedding vs RAG embedding distinction to embedding similarity.
- Added a fine-tuning troubleshooting segment to AdamW/lr.
- Added a LayerNorm/RMSNorm/Pre-Norm choice segment to normalization/residual/activation.
- Updated the reusable `knowledge-video-manim` skill with frame-boundary checking and rhythm guidance.

## Final Target

Final render target: 1280x720, 30 fps, narration audio, SRT subtitles, score >= 92/100 for each video.

## Final Review

| Video | Final Score | Reason |
| --- | ---: | --- |
| 机器学习与深度学习基础 | 93 | Covers the chapter map and clarifies training vs inference |
| 损失函数与交叉熵 | 94 | Explains intuition, formula, PPL, and SFT masking boundary |
| Embedding 与向量相似度 | 93 | Separates id, embedding, contextual representation, and retrieval embedding |
| AdamW 与学习率调度 | 92 | Covers update logic, AdamW, scheduling, stability tools, and fine-tuning diagnosis |
| 归一化、残差与激活函数 | 94 | Connects block structure, stability, residual learning, activation, and architecture tradeoffs |

All final videos passed artifact checks: 1280x720, 30 fps, audio track present, visible subtitles present, external SRT exported.
