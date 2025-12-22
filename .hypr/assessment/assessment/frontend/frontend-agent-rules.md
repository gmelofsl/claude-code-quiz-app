# Frontend Agent Implementation Rules

**IMPORTANT:** These rules are for Frontend Execute Agents working on specific chunks from a feature plan. For new features or complex changes, use the Plan Agent first (see ../../workflows/feature-flow.md).

## Per-File Implementation Loop

For EACH individual file, follow this exact sequence:

### Step 1: Pattern Check

- Review the pattern rules in frontend-agent.md for this file type
- Identify which specific rules apply to this file

### Step 2: Similar Files Analysis

- Find 3-5 existing files of the same type in the project
- Study their structure, naming, and implementation patterns
- Note the exact conventions they follow
- **NEVER assume components/imports exist - always verify exact names and paths**

### Step 3: Implement File

- **Check that all imports/components you want to use actually exist first**
- Create the single file following the patterns discovered
- Use the exact naming, structure, and style from similar files
- **Verify component names and import paths before using them**

### Step 4: Verify Pattern Match

- Compare the new file against the pattern rules in frontend-patterns.md
- Ensure it follows the same conventions as existing similar files
- **Verify file is in the correct folder** following project structure
- **Verify all imports are correct** and follow project import patterns
- Fix any deviations immediately

### Step 5: Verify Types

- **Use VSCode MCP server getDiagnostics if available** for efficient type checking
- If MCP not available, check that types compile correctly
- Ensure TypeScript (if used) passes for this file
- Fix any type errors

### Step 6: Write Test (MANDATORY if project has tests)

- **NEVER skip this step** - always check if similar files have tests
- If project has tests for similar files, **YOU MUST write test for this file**
- Follow the same testing patterns used in the project
- **Run the test for THIS FILE ONLY** to verify it passes

### Step 7: App Integration (for pages/features)

- **If creating a page component:** Add route to router configuration
- **If creating a page component:** Add navigation link if needed
- **If component needs data:** Implement API calls following project patterns
- **If component needs data:** Add proper loading/error states
- **If feature requires permissions:** Check if existing permission applies or ask user if new permission needed
- Verify the feature works end-to-end in the app

### Step 8: Final Validation, Verification and Documentation

- **Use VSCode MCP server getDiagnostics if available** for final type/lint checking
- **Run linting tools on this single file** - must pass
- **Run type checking on this single file** - must pass
- Verify the file integrates with existing code
- **Verify pattern compliance:** Confirm this file follows ALL applicable pattern rules
- **Verify requirements:** Confirm this file meets the original feature requirements
- **Document the feature:** Create/update documentation following project documentation patterns
- **ONLY IF ALL CHECKS PASS:** Mark this file as truly complete

## CRITICAL: ONE FILE AT A TIME ONLY

- **NEVER create multiple files in one response**
- **NEVER say "Now let me create the next component"**
- **COMPLETE ALL 8 STEPS for the current file BEFORE even mentioning another file**
- **MUST run lint and type check on THIS FILE before moving on**
- **MUST run any tests written for THIS FILE before moving on**
- Each file must go through: pattern check → analysis → implement → verify → types → test → integrate → final validation & documentation
- Only after all 8 steps pass completely should you consider the next file
