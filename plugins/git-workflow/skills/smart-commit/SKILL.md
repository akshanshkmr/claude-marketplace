---
name: smart-commit
description: Stage and commit changes with an auto-generated conventional commit message. Use when the user wants to commit, save changes, or create a commit.
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git diff *) Bash(git status *) Bash(git commit *)
---

## Current changes

!`git diff HEAD`

## Staged changes

!`git diff --cached`

## Instructions

1. Review the diff above.
2. Stage all relevant changes with `git add`.
3. Write a conventional commit message following this format:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `refactor:` for refactoring
   - `docs:` for documentation
   - `test:` for tests
   - `chore:` for maintenance tasks
4. Keep the subject line under 72 characters.
5. Add a short body if the change needs explanation.
6. Run `git commit -m "<message>"`.

If `$ARGUMENTS` is provided, use it as a hint for the commit message or scope.
