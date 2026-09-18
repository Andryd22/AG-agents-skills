---
name: parallel-agents
description: Multi-agent orchestration patterns. Use when multiple independent tasks can run with different domain expertise or when comprehensive analysis requires multiple perspectives.
---

# Native Parallel Agents

> Orchestration through Antigravity's `invoke_subagent` tool

## Overview

This skill coordinates the kit's specialized agents, which are Antigravity custom agents in `.agents/agents/`, through `invoke_subagent`. Each subagent starts with a clean context (none of this conversation), gets only the tools and skills in its frontmatter, and returns its result to the caller. Where custom agents are not available (the Antigravity IDE until it supports them), read `.agents/agents/<name>.md` and apply it yourself, one domain at a time.

## When to Use Orchestration

✅ **Good for:**
- Complex tasks requiring multiple expertise domains
- Code analysis from security, performance, and quality perspectives
- Comprehensive reviews (architecture + security + testing)
- Feature implementation needing backend + frontend + database work

❌ **Not for:**
- Simple, single-domain tasks
- Quick fixes or small changes
- Tasks where one agent suffices

---

## Native Agent Invocation

### Single Agent
```
Use the backend-specialist agent to review authentication for vulnerabilities
```

### Sequential Chain
```
First, use the explorer-agent to discover project structure.
Then, use the backend-specialist to review API endpoints.
Finally, use the test-engineer to identify test gaps.
```

### With Context Passing
```
Use the frontend-specialist to analyze React components.
Based on those findings, have the test-engineer generate component tests.
```

### Continue Previous Work
```
Send a follow-up message to the same subagent: it keeps its own context and wakes up when it receives the message.
```

---

## Orchestration Patterns

### Pattern 1: Comprehensive Analysis
```
Agents: explorer-agent → [domain-agents] → synthesis

1. explorer-agent: Map codebase structure
2. backend-specialist: API quality and security posture
3. frontend-specialist: UI/UX patterns
4. test-engineer: Test coverage
5. Synthesize all findings
```

### Pattern 2: Feature Review
```
Agents: affected-domain-agents → test-engineer

1. Identify affected domains (backend? frontend? both?)
2. Invoke relevant domain agents
3. test-engineer verifies changes
4. Synthesize recommendations
```

### Pattern 3: Security Review
```
Agents: explorer-agent → backend-specialist → synthesis

1. explorer-agent: Map auth, secrets, configuration and deployment files
2. backend-specialist: Auth, input validation, data access, secrets and deployment surface
3. Synthesize with prioritized remediation
```

---

## Available Agents

The complete list of agents, their domains and trigger keywords lives in `@[skills/intelligent-routing]` (section "Agent Selection Matrix"). Use that table instead of keeping a second copy here.

Antigravity also has built-in subagents (`research` for codebase exploration, `browser` for web testing): use them for quick searches and the kit's agents for domain expertise.

---

## Synthesis Protocol

After all agents complete, synthesize:

```markdown
## Orchestration Synthesis

### Task Summary
[What was accomplished]

### Agent Contributions
| Agent | Finding |
|-------|---------|
| backend-specialist | Found X |
| test-engineer | Identified Y |

### Consolidated Recommendations
1. **Critical**: [Issue from Agent A]
2. **Important**: [Issue from Agent B]
3. **Nice-to-have**: [Enhancement from Agent C]

### Action Items
- [ ] Fix critical security issue
- [ ] Refactor API endpoint
- [ ] Add missing tests
```

---

## Best Practices

1. **Available agents** - every agent listed in `@[skills/intelligent-routing]` can be orchestrated
2. **Logical order** - Discovery → Analysis → Implementation → Testing
3. **Share context** - Pass relevant findings to subsequent agents
4. **Single synthesis** - One unified report, not separate outputs
5. **Verify changes** - Always include test-engineer for code modifications

---

## Key Benefits

- ✅ **Clean contexts** - Each agent sees only the prompt you pass, so pass the full context
- ✅ **AI-controlled** - The model orchestrates autonomously
- ✅ **Native integration** - Works alongside Antigravity's built-in subagents
- ✅ **Follow-ups** - A subagent can receive further messages and continue its work
- ✅ **Context passing** - Findings flow between agents
