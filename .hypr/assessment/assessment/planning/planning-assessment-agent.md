# Planning Agent Assessment for AI Agents

## Core Principle

Extract NUMBERED RULES about how THIS PROJECT builds features at a high level. Rules must be specific to how THIS codebase approaches feature development, not generic software development advice.

## Step 0: Create Agent File First (MANDATORY)

**BEFORE doing any pattern analysis, create the agent implementation file:**

Copy the contents of `planning-agent-rules.md` from the assessment folder to create `planning-agent.md` in the `context/` folder.

## Assessment Process

Use this aspect-by-aspect approach to build the rules incrementally:

### PART 1: FEATURE ARCHITECTURE (Complete First 6 Aspects)

**DO ONE ASPECT AT A TIME - NEVER ANALYZE MULTIPLE ASPECTS TOGETHER**

#### Aspect 1: Feature Planning Structure

1. Look at 5-10 existing features in the project
2. Identify how features are organized and broken down
3. **IMMEDIATELY write 2-5 rules to the planning-agent.md file**
4. **ONLY AFTER writing rules** - move to Aspect 2

#### Aspect 2: Database and Migration Patterns

1. Look at how database changes are planned and implemented
2. Identify migration patterns, timing, and dependencies
3. **IMMEDIATELY write 2-5 rules to the planning-agent.md file**
4. **ONLY AFTER writing rules** - move to Aspect 3

#### Aspect 3: Frontend-Backend Integration

1. Look at how frontend and backend work together
2. Identify API design patterns, data flow, and coordination
3. **IMMEDIATELY write 2-5 rules to the planning-agent.md file**
4. **ONLY AFTER writing rules** - move to Aspect 4

#### Aspect 4: Testing Strategy and Timing

1. Look at how features are tested across the stack
2. Identify what gets tested when, and testing dependencies
3. **IMMEDIATELY write 2-5 rules to the planning-agent.md file**
4. **ONLY AFTER writing rules** - move to Aspect 5

#### Aspect 5: Page and Route Creation

1. Look at how new pages are added to the application
2. Identify routing patterns, navigation, and page structure
3. **IMMEDIATELY write 2-5 rules to the planning-agent.md file**
4. **ONLY AFTER writing rules** - move to Aspect 6

#### Aspect 6: Service Integration Patterns

1. Look at how features integrate with existing services
2. Identify service dependency patterns and integration points
3. **IMMEDIATELY write 2-5 rules to the planning-agent.md file**
4. **STOP HERE - ASK USER TO CONTINUE TO PART 2**

#### CRITICAL: Write Rules to File After Each Aspect

- **Write rules to planning-agent.md file immediately after each aspect**
- **NEVER analyze multiple aspects before writing rules to file**
- **STOP after Aspect 6 and ask user to continue**

---

### PART 2: IMPLEMENTATION PATTERNS (Continue After User Approval)

#### Aspect 7: Email and Notification Integration → write rules → next
#### Aspect 8: File Upload and Storage Integration → write rules → next
#### Aspect 9: Background Job Integration → write rules → next
#### Aspect 10: Caching Strategy Integration → write rules → next
#### Aspect 11: Security and Permissions Planning → write rules → next
#### Aspect 12: Configuration and Environment Planning → write rules → next
#### **STOP HERE - ASK USER TO CONTINUE TO PART 3**

---

### PART 3: DELIVERY PATTERNS (Final Part)

#### Aspect 13: Documentation Requirements → write rules → next
#### Aspect 14: Deployment and Release Planning → write rules → next
#### Aspect 15: Rollback and Recovery Planning → write rules → next
#### Aspect 16: Performance Considerations → write rules → next
#### Aspect 17: Monitoring and Observability → write rules → next
#### **COMPLETE - PERFORM FINAL QUALITY CHECK**

## Output Format (MANDATORY)

**AFTER creating the agent file**, ADD your pattern rules to the SAME `planning-agent.md` file in the `context/` folder by appending:

```markdown

## Feature Planning Patterns - [Project Name]

1. [Specific rule about how THIS project plans X, with actual feature examples]
2. [How THIS project breaks down Y differently than standard practices]  
3. [THIS project's unique approach to feature Z with real examples]
...
25. [Minimum 25 PROJECT-SPECIFIC rules total]
```

## Critical Requirements

1. **Simple numbered list format** - no complex formatting
2. **Use ONLY real project feature examples** - never generic examples
3. **Include actual file paths and feature names** where examples are found
4. **Extract minimum 25 rules** - aim for comprehensive coverage
5. **Rules must be PROJECT-SPECIFIC** - how THIS codebase plans features
6. **Rules must be actionable** - specific enough to follow immediately

## Final Quality Check (MANDATORY)

After creating all rules, perform this comprehensive review:

### Rule Quality Validation

Go through each rule and verify:

- [ ] Rule is specific to THIS project (not generic feature planning advice)
- [ ] Rule includes actual feature examples and file paths
- [ ] Rule is actionable (specific enough to follow immediately)
- [ ] Rule shows project-specific patterns, not best practices

### Coverage Validation

Check that rules comprehensively cover:

- [ ] Feature planning structure (2-5 rules)
- [ ] Database and migration patterns (2-5 rules)
- [ ] Frontend-backend integration (2-5 rules)
- [ ] Testing strategy and timing (2-5 rules)
- [ ] Page and route creation (2-5 rules)
- [ ] Service integration patterns (2-5 rules)
- [ ] Email and notification integration (2-5 rules)
- [ ] File upload and storage integration (2-5 rules)
- [ ] Background job integration (2-5 rules)
- [ ] Caching strategy integration (2-5 rules)
- [ ] Security and permissions planning (2-5 rules)
- [ ] Configuration and environment planning (2-5 rules)
- [ ] Documentation requirements (2-5 rules)
- [ ] Deployment and release planning (2-5 rules)
- [ ] Rollback and recovery planning (2-5 rules)
- [ ] Performance considerations (2-5 rules)
- [ ] Monitoring and observability (2-5 rules)

### Completeness Test

- [ ] Minimum 25 rules total
- [ ] Each rule addresses a specific, observable pattern from the codebase
- [ ] Rules work together to enable creating project-consistent feature plans
- [ ] No major feature planning aspect is missing from the rules

### Final Verification

- [ ] **Could a new AI agent create feature plans indistinguishable from existing project planning using ONLY these rules?**
- [ ] **Are there any gaps that would lead to incorrect feature breakdowns?**
- [ ] **Do the rules capture the project's unique approach vs standard planning practices?**

## Success Test

An AI agent should be able to create feature plans that follow this project's specific patterns and result in features that integrate seamlessly with the existing codebase using only the numbered rules from this assessment.