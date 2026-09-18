---
name: html-it
description: Trigger the html-it skill to output a high-fidelity HTML artifact instead of markdown.
---

# /html-it

Use this command when you want the agent to produce a rich, interactive, or highly structured HTML artifact instead of standard markdown.

## Flow

1. Analyzes the user's request to determine the appropriate HTML level (Static Doc, Visual Artifact, Interactive, Throwaway Tool).
2. Loads the `html-it` skill.
3. Generates a standalone, single-file HTML document matching the requirements.

## Usage

```
/html-it create a summary of the project architecture
/html-it turn these lecture notes into an interactive study guide
```
