#!/usr/bin/env node

import { spawn } from "node:child_process";

const prompt = process.argv.slice(2).join(" ").trim();

if (!prompt) {
  console.error('Usage: node scripts/call-claude-acp.mjs "你的问题"');
  process.exit(1);
}

const args = [
  "acpx",
  "--format",
  process.env.ACPX_FORMAT || "quiet",
  "claude",
  "exec",
  prompt,
];

const child = spawn("npx", args, {
  stdio: "inherit",
  env: process.env,
});

child.on("error", (error) => {
  console.error(`Failed to start acpx: ${error.message}`);
  process.exit(1);
});

child.on("close", (code, signal) => {
  if (signal) {
    console.error(`acpx was stopped by ${signal}`);
    process.exit(1);
  }

  process.exit(code ?? 1);
});
