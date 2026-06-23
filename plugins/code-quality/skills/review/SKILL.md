---
name: review
description: Review code for bugs, security issues, performance problems, and best practices. Use when the user asks to review code, check for issues, or audit a file.
argument-hint: [file or description]
---

## Instructions

Review $ARGUMENTS (or the recently edited files if no argument given) for:

### Correctness
- Logic errors, off-by-one errors, null/undefined handling
- Edge cases that could cause failures

### Security
- Input validation and sanitization
- Injection vulnerabilities (SQL, command, XSS)
- Hardcoded secrets or credentials
- Insecure defaults

### Performance
- Unnecessary loops or re-computation
- Missing indexes or caching opportunities
- Memory leaks

### Best practices
- Error handling and logging
- Code readability and naming
- Missing or incorrect types
- Test coverage gaps

Format your response as:
- **Critical** issues first (bugs, security)
- **Suggestions** for improvements
- **Looks good** for any areas that are clean

Be concise and actionable. Skip areas that are clean.
