# Quiz questions covering AI software development concepts with Claude Code

QUIZ_DATA = [
    # Topic 1: CLAUDE.md
    {
        "topic": "CLAUDE.md",
        "question": "What is the primary purpose of the CLAUDE.md file?",
        "options": [
            "To store Claude's conversation history",
            "To provide project context and instructions to Claude Code",
            "To configure Claude Code settings",
            "To document API endpoints"
        ],
        "correct": 1,
        "explanation": "CLAUDE.md serves as a context file that provides Claude with project-specific information, coding standards, architecture details, and instructions."
    },
    {
        "topic": "CLAUDE.md",
        "question": "Which of the following should you include in CLAUDE.md?",
        "options": [
            "Passwords and API keys",
            "Project structure, coding conventions, and common patterns",
            "Complete source code of all files",
            "Binary files and images"
        ],
        "correct": 1,
        "explanation": "CLAUDE.md should contain high-level project context like structure, conventions, patterns, and guidelines - not secrets or complete source code."
    },

    # Topic 2: Agents
    {
        "topic": "Agents",
        "question": "When should you use the Task tool with specialized agents?",
        "options": [
            "Only when the user explicitly asks for it",
            "For simple single-file edits",
            "For complex multi-step tasks or codebase exploration",
            "Never, always do the work yourself"
        ],
        "correct": 2,
        "explanation": "Specialized agents (like Explore, Plan) are designed for complex tasks, multi-file operations, and thorough codebase analysis that would be inefficient to do directly."
    },
    {
        "topic": "Agents",
        "question": "What is the benefit of launching multiple agents concurrently?",
        "options": [
            "It reduces token usage",
            "It maximizes performance by parallelizing independent tasks",
            "It prevents errors",
            "It makes debugging easier"
        ],
        "correct": 1,
        "explanation": "Launching agents concurrently (in a single message with multiple Task calls) maximizes performance by allowing independent tasks to run in parallel."
    },

    # Topic 3: Custom Commands
    {
        "topic": "Custom Commands",
        "question": "Where should you store custom slash commands?",
        "options": [
            "In the root directory",
            "In .claude/commands/ directory",
            "In package.json",
            "In settings.json"
        ],
        "correct": 1,
        "explanation": "Custom slash commands are stored as markdown files in the .claude/commands/ directory."
    },
    {
        "topic": "Custom Commands",
        "question": "When should you create a custom command?",
        "options": [
            "For every single task you do",
            "For repetitive workflows or team-shared processes",
            "Only for git operations",
            "Never, built-in commands are sufficient"
        ],
        "correct": 1,
        "explanation": "Custom commands are valuable for repetitive workflows, team-shared processes, and standardizing common operations across your team."
    },

    # Topic 4: Planning Workflow
    {
        "topic": "Planning Workflow",
        "question": "What is the primary benefit of using Plan Mode before coding?",
        "options": [
            "It makes the code run faster",
            "It prevents Claude from reading files",
            "It allows safe exploration and strategy review before making changes",
            "It automatically fixes bugs"
        ],
        "correct": 2,
        "explanation": "Plan Mode lets Claude analyze and design implementation approaches without making changes, allowing you to review and approve the strategy first."
    },
    {
        "topic": "Planning Workflow",
        "question": "When should you use EnterPlanMode?",
        "options": [
            "Only for fixing typos",
            "For new features, refactors, and tasks with multiple valid approaches",
            "After code is already written",
            "Only when explicitly asked by the user"
        ],
        "correct": 1,
        "explanation": "EnterPlanMode is recommended for non-trivial tasks like new features, refactors, architectural decisions, and anything with multiple implementation approaches."
    },

    # Topic 5: Model Selection
    {
        "topic": "Model Selection",
        "question": "Which Claude model should you use for quick, straightforward tasks?",
        "options": [
            "Opus - it's always the best",
            "Haiku - to minimize cost and latency",
            "Sonnet - for everything",
            "It doesn't matter"
        ],
        "correct": 1,
        "explanation": "Haiku is preferred for quick, straightforward tasks to minimize cost and latency, while Sonnet/Opus are better for complex reasoning."
    },
    {
        "topic": "Model Selection",
        "question": "How do you switch models in Claude Code?",
        "options": [
            "Restart the application",
            "Edit a configuration file manually",
            "Use the /model command",
            "You cannot switch models"
        ],
        "correct": 2,
        "explanation": "You can switch models during a session using the /model command to select between Sonnet, Opus, or Haiku."
    },

    # Topic 6: Context Management
    {
        "topic": "Context Management",
        "question": "What does the /clear command do?",
        "options": [
            "Deletes all files in the project",
            "Clears the conversation history and context",
            "Clears only the terminal screen",
            "Resets Claude's memory permanently"
        ],
        "correct": 1,
        "explanation": "/clear clears the conversation history and context, giving you a fresh start while keeping your files unchanged."
    },
    {
        "topic": "Context Management",
        "question": "What happens to context in Claude Code?",
        "options": [
            "It's limited to 200k tokens and then fails",
            "It uses automatic summarization for unlimited context",
            "Context is never tracked",
            "You must manually clear it every 5 messages"
        ],
        "correct": 1,
        "explanation": "Claude Code uses automatic summarization to provide unlimited context, so you never hit hard limits."
    },

    # Topic 7: Permissions
    {
        "topic": "Permissions",
        "question": "Which tools require permission approval?",
        "options": [
            "All tools including Read",
            "Only Bash commands",
            "Bash commands and file modifications (Edit/Write)",
            "No tools require permission"
        ],
        "correct": 2,
        "explanation": "Read-only tools (Read, Grep, Glob) don't require permission, but Bash commands and file modifications do."
    },
    {
        "topic": "Permissions",
        "question": "What should you auto-approve in permissions?",
        "options": [
            "All bash commands for convenience",
            "Safe commands like builds, tests, and git status",
            "Network requests and destructive operations",
            "Commands that modify .env files"
        ],
        "correct": 1,
        "explanation": "Auto-approve safe, repetitive commands like builds, tests, and git status. Always manually review destructive operations and network requests."
    },

    # Topic 8: Review Process
    {
        "topic": "Review Process",
        "question": "What keyboard shortcut opens the rewind menu?",
        "options": [
            "Ctrl+Z",
            "Esc + Esc",
            "Shift+R",
            "Alt+R"
        ],
        "correct": 1,
        "explanation": "Pressing Esc + Esc opens the rewind menu, allowing you to undo conversation and/or code changes."
    },
    {
        "topic": "Review Process",
        "question": "How do checkpoints work in Claude Code?",
        "options": [
            "You must manually create them",
            "They're created automatically at each user prompt",
            "They only work with git commits",
            "They expire after 5 minutes"
        ],
        "correct": 1,
        "explanation": "Claude Code automatically creates checkpoints at each user prompt, persisting for 30 days."
    },

    # Topic 9: MCP
    {
        "topic": "MCP",
        "question": "What does MCP stand for?",
        "options": [
            "Multi-Code Protocol",
            "Model Context Protocol",
            "Machine Control Program",
            "Master Configuration Process"
        ],
        "correct": 1,
        "explanation": "MCP stands for Model Context Protocol, a standard for connecting AI assistants to external tools and data sources."
    },
    {
        "topic": "MCP",
        "question": "What is the primary benefit of MCP servers?",
        "options": [
            "They make code run faster",
            "They extend Claude's capabilities with external tools and data sources",
            "They reduce token costs",
            "They store your conversation history"
        ],
        "correct": 1,
        "explanation": "MCP servers allow Claude to connect to external tools, APIs, databases, and data sources, extending its capabilities beyond built-in tools."
    },
]

def get_all_topics():
    """Get list of all unique topics"""
    return list(set(q["topic"] for q in QUIZ_DATA))

def get_questions_by_topic(topic):
    """Get all questions for a specific topic"""
    return [q for q in QUIZ_DATA if q["topic"] == topic]

def get_total_questions():
    """Get total number of questions"""
    return len(QUIZ_DATA)
