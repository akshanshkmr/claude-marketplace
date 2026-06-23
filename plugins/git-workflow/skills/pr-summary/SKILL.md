---
name: pr-summary
description: Summarize the current branch's changes relative to main for a pull request description. Use when the user wants to write a PR description, open a PR, or summarize what changed.
context: fork
agent: Explore
allowed-tools: Bash(git *)
---

## Branch diff

!`git log --oneline $(git merge-base HEAD main)..HEAD`

## Changed files

!`git diff --stat $(git merge-base HEAD main)..HEAD`

## Full diff

!`git diff $(git merge-base HEAD main)..HEAD`

## Instructions

Write a concise pull request description with:

1. **Summary** — 1–2 sentences describing what this PR does and why.
2. **Changes** — bullet list of the key modifications.
3. **Test plan** — how to verify the changes work.

Keep the summary under 80 words. Focus on the "why", not the "what" (the diff already shows the what).

If $ARGUMENTS is provided, treat it as additional context about the PR.
