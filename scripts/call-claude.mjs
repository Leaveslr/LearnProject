#!/usr/bin/env node

const apiKey = process.env.ANTHROPIC_API_KEY;
const model = process.env.CLAUDE_MODEL || "claude-sonnet-4-5-20250929";
const maxTokens = Number(process.env.CLAUDE_MAX_TOKENS || 1024);
const prompt = process.argv.slice(2).join(" ").trim();

if (!apiKey) {
  console.error("Missing ANTHROPIC_API_KEY. Example:");
  console.error('  ANTHROPIC_API_KEY="sk-ant-..." node scripts/call-claude.mjs "你好"');
  process.exit(1);
}

if (!prompt) {
  console.error('Usage: node scripts/call-claude.mjs "你的问题"');
  process.exit(1);
}

const response = await fetch("https://api.anthropic.com/v1/messages", {
  method: "POST",
  headers: {
    "content-type": "application/json",
    "x-api-key": apiKey,
    "anthropic-version": "2023-06-01",
  },
  body: JSON.stringify({
    model,
    max_tokens: maxTokens,
    messages: [
      {
        role: "user",
        content: prompt,
      },
    ],
  }),
});

const payload = await response.json().catch(() => null);

if (!response.ok) {
  console.error(`Claude API error: ${response.status} ${response.statusText}`);
  console.error(JSON.stringify(payload, null, 2));
  process.exit(1);
}

const text = payload.content
  ?.filter((item) => item.type === "text")
  .map((item) => item.text)
  .join("\n");

console.log(text || JSON.stringify(payload, null, 2));
