# Project Assessment System for AI Agents

A comprehensive system for enabling AI agents to understand and follow project-specific patterns when building features.

## Overview

This assessment system creates specialized AI agents that understand how YOUR specific project works, not just generic best practices. It ensures AI-generated code is indistinguishable from code written by your original development team.

## Three-Agent Architecture

### 1. Planning Agent

**Purpose**: Create detailed feature plans and break them into implementable chunks

**Created by**: `planning/planning-assessment-agent.md` → `planning-agent.md`

- Discovers how your project plans and structures features
- Learns your database migration patterns
- Understands your testing strategies and timing
- Maps your service integration approaches
- Creates actionable feature documents with clear chunk breakdown

### 2. Frontend Execute Agent

**Purpose**: Implement frontend chunks with strict pattern validation

**Created by**: `frontend/frontend-assessment-agent.md` → `frontend-agent.md`

- Learns your component structure and naming conventions
- Discovers your styling and theming patterns
- Maps your state management approaches
- Understands your routing and navigation patterns
- Follows 8-step per-file validation process

### 3. Backend Execute Agent

**Purpose**: Implement backend chunks with strict pattern validation

**Created by**: `backend/backend-assessment-agent.md` → `backend-agent.md`

- Learns your API endpoint structure and naming
- Discovers your database query patterns
- Maps your authentication and authorization approaches
- Understands your service organization
- Follows 7-step per-file validation process

## Workflow

```
User Feature Request
        ↓
    Planning Agent
  (creates feature doc)
        ↓
   Feature Document
   (with small chunks)
        ↓
  ┌─────────────────┐
  ↓                 ↓
Frontend Agent    Backend Agent
(chunk by chunk)  (chunk by chunk)
```

## Assessment Files

### Core Assessments

- `planning/planning-assessment-agent.md` - Discovers feature planning patterns
- `frontend/frontend-assessment-agent.md` - Discovers frontend implementation patterns
- `backend/backend-assessment-agent.md` - Discovers backend implementation patterns

### Agent Implementation Rules

- `planning/planning-agent-rules.md` - Planning process and feature document creation
- `frontend/frontend-agent-rules.md` - 8-step frontend implementation process
- `backend/backend-agent-rules.md` - 7-step backend implementation process

### Orchestration

- `../workflows/feature-flow.md` - Explains when to use which agent
- `README.md` - This overview document

## Key Features

### Part-by-Part Assessment

- **Never overwhelm** - Break assessment into digestible chunks (6 + 6 + 5 aspects)
- **User checkpoints** - Stop and ask for approval between parts
- **Immediate rule writing** - Write rules to file after each aspect
- **No batching** - One aspect at a time, always

### Project-Specific Rules

- **Real code examples only** - Never generic patterns
- **Actual file paths** - Reference existing project files
- **Wrong vs Right format** - Show violations and correct implementations
- **Actionable guidance** - Specific enough to follow immediately

### Strict Validation

- **Per-file discipline** - Complete one file before starting next
- **Pattern compliance** - Verify against extracted rules
- **Type checking** - Use VSCode MCP server when available
- **Testing requirements** - Mandatory tests when project has them
- **Integration verification** - Ensure files work with existing code

## Getting Started

### Step 1: Run Assessments

1. Run `planning/planning-assessment-agent.md` to create planning agent
2. Run `frontend/frontend-assessment-agent.md` to create frontend agent
3. Run `backend/backend-assessment-agent.md` to create backend agent

### Step 2: Build Features

1. Use Planning Agent for new features → creates feature document
2. Use Execute Agents for chunks → implements following strict patterns
3. Validate each chunk → ensures quality and consistency

## Benefits

- **Consistent Code**: Generated code matches existing project style exactly
- **No Context Loss**: Project patterns captured in permanent rules
- **Scalable**: New team members use same patterns via agents
- **Quality Gates**: Built-in validation prevents pattern violations
- **Maintainable**: Rules update as project patterns evolve

## File Structure After Assessment

```
project-root/
├── context/
│   ├── planning-agent.md      # Planning rules + project patterns
│   ├── frontend-agent.md      # Frontend rules + project patterns
│   └── backend-agent.md       # Backend rules + project patterns
├── features/
│   ├── feature-001.md         # Feature plans created by Planning Agent
│   ├── feature-002.md
│   └── ...
└── assessment/               # This folder - assessment methodology
    ├── README.md            # This file
    ├── planning/
    │   ├── planning-assessment-agent.md
    │   └── planning-agent-rules.md
    ├── frontend/
    │   ├── frontend-assessment-agent.md
    │   └── frontend-agent-rules.md
    └── backend/
        ├── backend-assessment-agent.md
        └── backend-agent-rules.md
```

## Success Criteria

When working correctly:

- AI agents create code indistinguishable from existing project code
- Features integrate seamlessly with existing systems
- No additional research needed beyond context files
- New team members can build features following project patterns exactly
- Code reviews focus on business logic, not style/pattern violations
