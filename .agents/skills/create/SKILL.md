---
name: create
description: 'Create a new application from a description: clarify what is missing, plan with project-planner, build with app-builder and the specialist agents, then start a preview. Use when the user runs /create or asks to build a new app from scratch.'
---

# /create - Create Application

The request is the text that follows `/create`.

---

## Task

This command starts a new application creation process.

### Steps

1. **Request Analysis**
   - Understand what the user wants
   - If information is missing, ask using the `brainstorm` skill (Socratic Gate)

2. **Project Planning**
   - Use `project-planner` agent for task breakdown
   - Determine tech stack
   - Plan file structure
   - Create plan file and proceed to building

3. **Application Building (After Approval)**
   - Orchestrate with `app-builder` skill
   - Coordinate expert agents:
     - `backend-specialist` → Schema and API
     - `frontend-specialist` → UI

4. **Preview**
   - Start with `auto_preview.py` when complete
   - Present URL to user

---

## Usage Examples

```text
/create blog site
/create e-commerce app with product listing and cart
/create todo app
/create Instagram clone
/create crm system with customer management
```

---

## Before Starting

If request is unclear, ask these questions:

- What type of application?
- What are the basic features?
- Who will use it?

Use defaults, add details later.
