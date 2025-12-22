# Frontend Patterns Assessment for AI Agents

## Core Principle

Extract NUMBERED RULES from THIS PROJECT'S actual code patterns. Rules must be specific to how THIS codebase works, not generic React/frontend advice.

## Step 0: Create Agent File First (MANDATORY)

**BEFORE doing any pattern analysis, create the agent implementation file:**

Copy the contents of `frontend-agent-rules.md` from the assessment folder to create `frontend-agent.md` in the `context/` folder.

## Assessment Process

Use this aspect-by-aspect approach to build the rules incrementally:

### PART 1: CORE PATTERNS (Complete First 6 Aspects)

**DO ONE ASPECT AT A TIME - NEVER ANALYZE MULTIPLE ASPECTS TOGETHER**

#### Aspect 1: Component Structure and Naming
1. Look at 5-10 component files
2. Identify naming patterns, file structure, export patterns
3. **IMMEDIATELY write 2-5 rules to the frontend-agent.md file**
4. **ONLY AFTER writing rules** - move to Aspect 2

#### Aspect 2: File Organization  
1. Look at folder structure and file placement patterns
2. Identify organization principles used
3. **IMMEDIATELY write 2-5 rules to the frontend-agent.md file**
4. **ONLY AFTER writing rules** - move to Aspect 3

#### Aspect 3: Styling Approach
1. Look at how styling is implemented across files
2. Identify consistent styling patterns
3. **IMMEDIATELY write 2-5 rules to the frontend-agent.md file**  
4. **ONLY AFTER writing rules** - move to Aspect 4

#### Aspect 4: State Management
1. Look at how state is managed across components
2. Identify state management patterns used
3. **IMMEDIATELY write 2-5 rules to the frontend-agent.md file**
4. **ONLY AFTER writing rules** - move to Aspect 5

#### Aspect 5: Props and Data Flow  
1. Look at how props are passed and data flows
2. Identify data flow patterns used
3. **IMMEDIATELY write 2-5 rules to the frontend-agent.md file**
4. **ONLY AFTER writing rules** - move to Aspect 6

#### Aspect 6: Import/Export Patterns
1. Look at how imports and exports are organized
2. Identify import/export patterns used
3. **IMMEDIATELY write 2-5 rules to the frontend-agent.md file**
4. **STOP HERE - ASK USER TO CONTINUE TO PART 2**

#### CRITICAL: Write Rules to File After Each Aspect
- **Write rules to frontend-agent.md file immediately after each aspect**
- **NEVER analyze multiple aspects before writing rules to file**
- **STOP after Aspect 6 and ask user to continue**

---

### PART 2: ADVANCED PATTERNS (Continue After User Approval)

#### Aspect 7: Type Definitions and Language Patterns → write rules → next
#### Aspect 8: Error Handling → write rules → next
#### Aspect 9: Testing Patterns → write rules → next
#### Aspect 10: Form Handling and Validation → write rules → next
#### Aspect 11: Data Fetching and API Integration → write rules → next
#### Aspect 12: Routing and Navigation Integration → write rules → next
#### **STOP HERE - ASK USER TO CONTINUE TO PART 3**

---

### PART 3: INTEGRATION PATTERNS (Final Part)

#### Aspect 13: Permissions and Security Patterns → write rules → next
#### Aspect 14: Performance Optimization Patterns → write rules → next
#### Aspect 15: Configuration Management → write rules → next
#### Aspect 16: Documentation Patterns → write rules → next
#### Aspect 17: Build/Tooling → write rules → next
#### **COMPLETE - PERFORM FINAL QUALITY CHECK**

## Output Format (MANDATORY)

**AFTER creating the agent file**, ADD your pattern rules to the SAME `frontend-agent.md` file in the `context/` folder by appending:

```markdown

## Frontend Patterns - [Project Name]

1. [Specific rule about how THIS project does X, with actual file examples]
2. [How THIS project handles Y differently than standard practices]
3. [THIS project's unique approach to Z with code examples]
...
25. [Minimum 25 PROJECT-SPECIFIC rules total]

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
- [ ] Rule is specific to THIS project (not generic React advice)
- [ ] Rule includes actual file paths as examples
- [ ] Rule is actionable (specific enough to follow immediately)
- [ ] Rule shows project-specific patterns, not best practices

### Coverage Validation
Check that rules comprehensively cover:
- [ ] Component structure and naming (2-5 rules)
- [ ] File organization (2-5 rules)
- [ ] Styling approach (2-5 rules)
- [ ] State management (2-5 rules)
- [ ] Props and data flow (2-5 rules)
- [ ] Import/export patterns (2-5 rules)
- [ ] Type definitions and language patterns (2-5 rules)
- [ ] Error handling (2-5 rules)
- [ ] Testing patterns (2-5 rules)
- [ ] Form handling and validation (2-5 rules)
- [ ] Data fetching and API integration (2-5 rules)
- [ ] Routing and navigation integration (2-5 rules)
- [ ] Permissions and security patterns (2-5 rules)
- [ ] Performance optimization patterns (2-5 rules)
- [ ] Configuration management (2-5 rules)
- [ ] Documentation patterns (2-5 rules)
- [ ] Build/tooling integration (2-5 rules)

### Completeness Test
- [ ] Minimum 25 rules total
- [ ] Each rule addresses a specific, observable pattern from the codebase
- [ ] Rules work together to enable creating project-consistent components
- [ ] No major frontend aspect is missing from the rules

### Final Verification
- [ ] **Could a new AI agent create components indistinguishable from existing ones using ONLY these rules?**
- [ ] **Are there any gaps that would lead to incorrect implementations?**
- [ ] **Do the rules capture the project's unique approach vs standard practices?**

## Success Test

An AI agent should be able to create components that are indistinguishable from existing project components using only the numbered rules from this assessment.
