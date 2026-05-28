# Topic JSON Schema

Use one JSON file per video.

```json
{
  "slug": "kv_cache",
  "title": "KV Cache 机制",
  "segments": [
    {
      "duration": 8.0,
      "subtitle": "One readable narration/subtitle line.",
      "visual": {
        "type": "pipeline",
        "steps": ["A", "B", "C"],
        "caption": "Optional caption"
      }
    }
  ]
}
```

## Segment Rules

- `duration`: usually 6-9 seconds.
- `subtitle`: one to two short sentences.
- `visual.type`: choose from the supported visual types below.

## Visual Types

- `title`: `headline`, optional `subhead`.
- `compare`: `items` list of `{ "title": "...", "body": "..." }`.
- `pipeline`: `steps` list, optional `caption`.
- `tokens`: `tokens` list, optional `focus` index and `note`.
- `cache`: `before`, `cache`, `new`, optional `caption`.
- `loop`: `steps` list of four labels, optional `center`.
- `bars`: `items` list of `{ "label": "...", "value": 3, "text": "..." }`.
- `formula`: `formula`, `items` list of formula term cards.
- `trace`: `items` list of `{ "label": "Thought", "text": "..." }`.
- `summary`: `points` list.

## Concept-Specific Requirements

- Mechanism topics: include a small example and a formula breakdown if a formula exists.
- System optimization topics: include what is cached or reused, what cost remains, and a memory/performance boundary.
- Agent/workflow topics: include the loop, a concrete trace, failure modes, and stop conditions.
- Algorithm topics: include a toy input, state transitions, invariant or correctness intuition, and complexity only after the process is visible.
