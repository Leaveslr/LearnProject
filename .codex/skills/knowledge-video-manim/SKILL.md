---
name: knowledge-video-manim
description: Create beginner-friendly knowledge explainer videos with Manim, including teaching-logic research, structured script, narration, subtitles, rendered MP4, frame checks, and iterative expert evaluation. Use when Codex is asked to turn a technical concept, AI topic, algorithm, architecture, mechanism, or learning note into a reusable animated teaching video.
---

# Knowledge Video Manim

## Workflow

1. Research the teaching logic before writing visuals.
   - Identify the concept type: mechanism, system optimization, workflow, algorithm, comparison, or formula.
   - Extract what a beginner must understand: motivation, mental model, smallest example, formal rule, boundary, common mistake.
   - Use strong explainer patterns: problem first, terms late, one visual action per segment, formula only after the intuition has landed.

2. Write the segment script.
   - Keep each segment to 6-9 seconds and one cognitive action.
   - Use subtitle lines that can be read in one breath.
   - Use the core structure: minimal concept map, one running example, mechanism walk-through, key details, counterfactual/boundary, judgment questions, three-sentence summary.
   - Keep concept exposition short: about 15-20% of the video.
   - Make one example carry the main teaching load: about 55-65% of the video.
   - End with judgment questions, not memory questions: about 15-20% of the video.
   - Require these sections: hook, minimal concept, one running example, core mechanism, concrete walk-through, boundary or caveat, judgment questions, three-sentence summary.
   - For formulas, translate every term into plain language on screen.
   - Add numeric intuition when it helps the learner judge magnitude, such as comparing P=0.90, P=0.30, and P=0.01.

3. Build or edit a topic JSON.
   - Use `references/topic-schema.md` for the JSON format and supported visual types.
   - Prefer `title`, `compare`, `pipeline`, `trace`, `cache`, `formula`, `bars`, `loop`, and `summary` before writing a custom Manim scene.

4. Render with the bundled scripts when a generic visual grammar is enough.
   - Copy `scripts/generic_video.py` and `scripts/render_topic.py` into the project folder, or run them from the skill folder with a topic JSON.
   - Use the Codex bundled Python runtime or another Python that can import `numpy`, `scipy`, and `manim`.
   - Use `say` for quick Chinese narration and `ffmpeg` to convert audio to WAV.
   - Avoid `MathTex` and LaTeX unless TeX is installed; use normal `Text` formulas for portability.

5. Evaluate and iterate.
   - Read `references/rubric.md`.
   - Render a low-resolution preview first.
   - Extract 4-6 frames across the video and inspect text fit, overlap, visual clarity, and whether the frame is meaningful without audio.
   - Sample frames around likely segment boundaries; if several frames show only title/subtitle, shorten transition fades or lengthen visual holds before rendering the final version.
   - Judge learning by transfer: the learner should be able to say what the concept is, what the key details are, and why the design choice is made.
   - Require at least 2-3 judgment questions in the script. A video does not pass if the questions only test memorization.
   - Run at least two content-shape tests before trusting a reusable workflow: one mechanism/system topic and one workflow/Agent topic.
   - Iterate until the video is at least 90/100 or the remaining gap is explicitly production polish such as human voiceover.

6. Deliver the artifacts.
   - Return the MP4, SRT, topic JSON or script, source Manim files, and evaluation notes.
   - State resolution, duration, audio presence, and the final score.

## Practical Defaults

- Video: `1280x720`, 30 fps, short-form explainer length 90-150 seconds.
- Visual density: no more than 3 main objects or 1 small table per screen.
- Subtitle: bottom rounded band, present throughout the segment.
- Scene rhythm: keep the main visual visible for most of each narration segment; use quick fades so the learner rarely sees an empty stage.
- Formula: introduce after an example; split into action labels such as match, normalize, sum.
- Chinese narration: `say -v Tingting -r 175` is acceptable for preview; human voiceover can replace it later.
- Environment: keep virtual environments outside the repo when possible, such as `~/.cache/codex-manim-venv`.
