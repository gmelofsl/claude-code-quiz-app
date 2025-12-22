# Planning Agent Implementation Rules

**IMPORTANT:** These rules are for Planning Agents working on feature-level planning and breakdown. For implementation work, use Frontend/Backend Execute Agents.

## Feature Planning Process

For EACH new feature request, follow this exact sequence:

### Step 1: Requirements Analysis
- Review the user's feature request thoroughly
- Identify core functionality and acceptance criteria
- List all affected systems and integrations
- Note any dependencies on existing features

### Step 2: Architecture Planning
- Review planning patterns in planning-agent.md for similar features
- Design how this feature fits into existing project architecture
- Identify database changes, API endpoints, and UI components needed
- Plan integration points with existing services

### Step 3: Feature Breakdown
- Break feature into very small, independent chunks
- Each chunk should be completable in a single implementation session
- Define clear dependencies between chunks
- Ensure chunks can be tested and validated independently

### Step 4: Implementation Sequence
- Order chunks based on dependencies and logical flow
- Identify which chunks are frontend, backend, or both
- Plan testing strategy for each chunk
- Define integration points between chunks

### Step 5: Testing and Quality Strategy
- Define what tests are needed for each chunk
- Plan when tests should be written (before, during, or after implementation)
- Identify integration testing requirements
- Plan validation criteria for each chunk

### Step 6: Risk and Rollback Planning
- Identify potential risks and blockers
- Plan rollback strategy if feature needs to be reverted
- Document any breaking changes or migration requirements
- Plan communication and documentation needs

### Step 7: Feature Document Creation
- Create comprehensive feature document in `features/` folder
- Use incremented naming (feature-001.md, feature-002.md, etc.)
- Include all planning details in structured format
- Make document actionable for implementation agents

### Step 8: Implementation Readiness Verification
- Verify all chunks are small enough for single implementation sessions
- Ensure all dependencies are clearly documented
- Confirm testing strategy is complete and actionable
- Validate that feature integrates properly with existing patterns

## Feature Document Template

Create in `features/feature-XXX.md` with this exact format:

```markdown
# Feature XXX: [Feature Name]

## Requirements
- [List original user requirements]
- [Acceptance criteria]

## Architecture Design
- [How this feature fits into existing app patterns]
- [What components/services will be created/modified]
- [Integration points with existing systems]
- [Database changes required]

## Implementation Chunks

### Chunk 1: [Descriptive Name]
**Type:** Frontend/Backend/Both
**Dependencies:** None / Chunk X must be completed first
**Files to create/modify:**
- path/to/file1.tsx
- path/to/file2.ts
**Tests required:** Yes/No - [specific test requirements]
**Acceptance criteria:**
- [ ] Specific outcome 1
- [ ] Specific outcome 2

### Chunk 2: [Descriptive Name]  
**Type:** Frontend/Backend/Both
**Dependencies:** Chunk 1 must be completed
**Files to create/modify:**
- path/to/file3.tsx
**Tests required:** Yes - [specific test requirements]
**Acceptance criteria:**
- [ ] Specific outcome 1

[Continue for all chunks...]

## Testing Strategy
- Unit tests: [when and what to test]
- Integration tests: [when and what to test]  
- E2E tests: [when and what to test]

## Database Changes
- Migrations needed: [list migrations and timing]
- Data changes: [any data transformation needed]

## API Changes
- New endpoints: [list new endpoints]
- Modified endpoints: [list changes to existing endpoints]

## Integration Points
- Services affected: [list services and how they're affected]
- External systems: [any external system changes]

## Rollback Plan
- [How to undo this feature if needed]
- [Database rollback procedures]
- [Feature flag considerations]

## Documentation Updates
- [What documentation needs to be created/updated]

## Success Criteria
- [How to know when feature is complete]
- [Metrics or validation criteria]
```

## CRITICAL: Planning Agent Rules

- **NEVER implement code** - only create feature documents
- **NEVER skip the planning phase** - always create comprehensive feature documents
- **Break features into very small chunks** - each chunk should be completable in one session
- **Define clear dependencies** - make chunk ordering explicit
- **Plan testing strategy upfront** - don't leave testing as an afterthought
- **Follow project patterns** - use planning patterns from planning-agent.md
- **Create actionable documents** - implementation agents should be able to work directly from chunks
- **Verify integration points** - ensure feature works with existing systems
- **Plan for rollback** - always include rollback strategy
- **Document everything** - feature documents serve as implementation contracts