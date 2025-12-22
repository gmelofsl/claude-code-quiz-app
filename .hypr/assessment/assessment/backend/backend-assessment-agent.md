# Backend Patterns Assessment for AI Agents

## Core Principle

Extract NUMBERED RULES from THIS PROJECT'S actual backend code patterns. Rules must be specific to how THIS codebase works, not generic Node.js/backend advice.

## Step 0: Create Agent File First (MANDATORY)

**BEFORE doing any pattern analysis, create the agent implementation file:**

Copy the contents of `backend-agent-rules.md` from the assessment folder to create `backend-agent.md` in the `context/` folder.

## Assessment Process

Use this aspect-by-aspect approach to build the rules incrementally:

### PART 1: CORE PATTERNS (Complete First 6 Aspects)

**DO ONE ASPECT AT A TIME - NEVER ANALYZE MULTIPLE ASPECTS TOGETHER**

#### Aspect 1: API Endpoint Structure and Naming

1. Look at 5-10 API endpoint files
2. Identify naming patterns, route structure, response patterns
3. **IMMEDIATELY write 2-5 rules to the backend-agent.md file**
4. **ONLY AFTER writing rules** - move to Aspect 2

#### Aspect 2: File Organization and Folder Structure

1. Look at backend folder structure and file placement
2. Identify organization principles used
3. **IMMEDIATELY write 2-5 rules to the backend-agent.md file**
4. **ONLY AFTER writing rules** - move to Aspect 3

#### Aspect 3: Database Queries and Transactions

1. Look at how database interactions are implemented
2. Identify consistent query patterns and transaction handling
3. **IMMEDIATELY write 2-5 rules to the backend-agent.md file**
4. **ONLY AFTER writing rules** - move to Aspect 4

#### Aspect 4: Authentication and Authorization

1. Look at how auth is implemented across endpoints
2. Identify authentication and authorization patterns
3. **IMMEDIATELY write 2-5 rules to the backend-agent.md file**
4. **ONLY AFTER writing rules** - move to Aspect 5

#### Aspect 5: Request Validation

1. Look at how requests are validated
2. Identify validation patterns used
3. **IMMEDIATELY write 2-5 rules to the backend-agent.md file**
4. **ONLY AFTER writing rules** - move to Aspect 6

#### Aspect 6: Error Handling and Exceptions

1. Look at how errors are handled across the backend
2. Identify error handling patterns used
3. **IMMEDIATELY write 2-5 rules to the backend-agent.md file**
4. **STOP HERE - ASK USER TO CONTINUE TO PART 2**

#### CRITICAL: Write Rules to File After Each Aspect

- **Write rules to backend-agent.md file immediately after each aspect**
- **NEVER analyze multiple aspects before writing rules to file**
- **STOP after Aspect 6 and ask user to continue**

---

### PART 2: SERVICE PATTERNS (Continue After User Approval)

#### Aspect 7: Service and Controller Organization → write rules → next

#### Aspect 8: Database Migrations → write rules → next

#### Aspect 9: Async Operation Patterns → write rules → next

#### Aspect 10: Logging and Monitoring → write rules → next

#### Aspect 11: Testing Patterns → write rules → next

#### Aspect 12: Permissions and Security Patterns → write rules → next

#### **STOP HERE - ASK USER TO CONTINUE TO PART 3**

---

### PART 3: INTEGRATION PATTERNS (Final Part)

#### Aspect 13: Caching Patterns → write rules → next

#### Aspect 14: Background Jobs and Queues → write rules → next

#### Aspect 15: File Upload and Storage → write rules → next

#### Aspect 16: Email and Notification Patterns → write rules → next

#### Aspect 17: Rate Limiting and Throttling → write rules → next

#### Aspect 18: Configuration Management → write rules → next

#### Aspect 19: Documentation Patterns → write rules → next

#### Aspect 20: Type Definitions and Language Patterns → write rules → next

#### Aspect 21: Build/Deployment Integration → write rules → next

#### **COMPLETE - PERFORM FINAL QUALITY CHECK**

## Output Format (MANDATORY)

**AFTER creating the agent file**, ADD your pattern rules to the SAME `backend-agent.md` file in the `context/` folder by appending:

```markdown
## Backend Patterns - [Project Name]

1. [Specific rule about how THIS project does X, with actual file examples]
2. [How THIS project handles Y differently than standard practices]
3. [THIS project's unique approach to Z with code examples]
   ...
4. [Minimum 25 PROJECT-SPECIFIC rules total]
```

## Critical Requirements

1. **Simple numbered list format** - no complex formatting
2. **Use ONLY real project code examples** - never generic code
3. **Include actual file paths** where examples are found
4. **Extract minimum 25 rules** - aim for comprehensive coverage
5. **Rules must be PROJECT-SPECIFIC** - how THIS codebase does things, not best practices
6. **Rules must be actionable** - specific enough to follow immediately

## Final Quality Check (MANDATORY)

After creating all rules, perform this comprehensive review:

### Rule Quality Validation

Go through each rule and verify:

- [ ] Rule is specific to THIS project (not generic Node.js/backend advice)
- [ ] Rule includes actual file paths as examples
- [ ] Rule is actionable (specific enough to follow immediately)
- [ ] Rule shows project-specific patterns, not best practices

### Coverage Validation

Check that rules comprehensively cover:

- [ ] API endpoint structure and naming (2-5 rules)
- [ ] File organization and folder structure (2-5 rules)
- [ ] Database queries and transactions (2-5 rules)
- [ ] Authentication and authorization (2-5 rules)
- [ ] Request validation (2-5 rules)
- [ ] Error handling and exceptions (2-5 rules)
- [ ] Service and controller organization (2-5 rules)
- [ ] Database migrations (2-5 rules)
- [ ] Async operation patterns (2-5 rules)
- [ ] Logging and monitoring (2-5 rules)
- [ ] Testing patterns (2-5 rules)
- [ ] Permissions and security patterns (2-5 rules)
- [ ] Caching patterns (2-5 rules)
- [ ] Background jobs and queues (2-5 rules)
- [ ] File upload and storage (2-5 rules)
- [ ] Email and notification patterns (2-5 rules)
- [ ] Rate limiting and throttling (2-5 rules)
- [ ] Configuration management (2-5 rules)
- [ ] Documentation patterns (2-5 rules)
- [ ] Type definitions and language patterns (2-5 rules)
- [ ] Build/deployment integration (2-5 rules)

### Completeness Test

- [ ] Minimum 25 rules total
- [ ] Each rule addresses a specific, observable pattern from the codebase
- [ ] Rules work together to enable creating project-consistent backend code
- [ ] No major backend aspect is missing from the rules

### Final Verification

- [ ] **Could a new AI agent create backend code indistinguishable from existing code using ONLY these rules?**
- [ ] **Are there any gaps that would lead to incorrect implementations?**
- [ ] **Do the rules capture the project's unique approach vs standard practices?**

## Success Test

An AI agent should be able to create backend code that is indistinguishable from existing project code using only the numbered rules from this assessment.
