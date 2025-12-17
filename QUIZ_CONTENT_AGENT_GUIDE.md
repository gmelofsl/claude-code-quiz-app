# Quiz Content Agent Guide

## Overview

The **Quiz Content Agent** is a specialized AI assistant designed to help you create, validate, and manage quiz questions for the Flask Quiz App. It's powered by Claude and accessible via the `/quiz-content-agent` slash command.

## What Can It Do?

The Quiz Content Agent helps with:

1. ✍️ **Generate New Questions** - Create high-quality quiz questions on any AI/ML topic
2. ✅ **Validate Quality** - Review existing questions for clarity, accuracy, and educational value
3. 🔍 **Detect Duplicates** - Find similar or redundant questions in your question bank
4. 📊 **Analyze Distribution** - Check category and difficulty balance
5. 💡 **Review Explanations** - Improve question explanations for better learning

## How to Use It

### Basic Syntax

```bash
/quiz-content-agent [your task description]
```

### Example Commands

#### 1. Generate New Questions

```bash
/quiz-content-agent Generate 5 medium difficulty questions about RAG (Retrieval Augmented Generation) for the Model Selection category

/quiz-content-agent Create 3 hard questions about multi-agent coordination patterns

/quiz-content-agent I need 10 easy questions about basic prompt engineering concepts

/quiz-content-agent Generate questions about Claude API best practices for 2025
```

#### 2. Validate Existing Questions

```bash
/quiz-content-agent Review all Agent Fundamentals questions for quality issues

/quiz-content-agent Check if questions 15-20 in quiz_data.py are clear and unambiguous

/quiz-content-agent Validate the difficulty levels are accurate for Prompt Engineering questions

/quiz-content-agent Review question quality and suggest improvements
```

#### 3. Check for Duplicates

```bash
/quiz-content-agent Check for duplicate or very similar questions across all categories

/quiz-content-agent Are there any overlapping questions in the Agent Fundamentals category?

/quiz-content-agent Find questions that test the same concept
```

#### 4. Analyze Distribution

```bash
/quiz-content-agent Analyze the distribution of questions by category and difficulty

/quiz-content-agent What gaps exist in our question coverage?

/quiz-content-agent Show me the breakdown of easy/medium/hard questions

/quiz-content-agent Which topics are underrepresented?
```

#### 5. Improve Explanations

```bash
/quiz-content-agent Review and improve explanations for all Prompt Engineering questions

/quiz-content-agent The explanation for question 12 is unclear, can you rewrite it?

/quiz-content-agent Make the explanations more helpful and educational
```

## Current Quiz Structure

**Categories (3 total):**
- 🤖 **Agent Fundamentals** (8 questions)
- ✍️ **Prompt Engineering** (10 questions)
- 🎯 **Model Selection & Context Management** (7 questions)

**Total Questions:** 25

**Difficulty Levels:**
- **Easy**: Recall facts, basic concepts, definitions
- **Medium**: Application, analysis, comparison
- **Hard**: Synthesis, evaluation, edge cases

## Question Format

All questions must follow this exact format in `quiz_data.py`:

```python
{
    "category": "Agent Fundamentals",  # Must be one of 3 categories
    "question": "What is the main challenge with multi-agent systems?",
    "options": [
        "Communication overhead and coordination",
        "Lack of available frameworks",
        "They are too slow",
        "They require quantum computers"
    ],
    "correct": 0,  # Index 0-3
    "difficulty": "medium",  # easy, medium, or hard
    "explanation": "Multi-agent systems face challenges in coordinating actions and managing communication between agents, especially as the number of agents increases."
}
```

## Quality Standards

The agent ensures all questions meet these standards:

### ✅ Good Questions Have:
- Clear, unambiguous wording
- Exactly 4 options
- One definitively correct answer
- Three plausible but incorrect distractors
- Helpful 2-4 sentence explanation
- Appropriate difficulty level
- No grammatical errors
- Current, accurate information (as of 2025)

### ❌ Avoid:
- "All of the above" or "None of the above" options
- Trick questions
- Opinion-based questions
- Outdated information
- Overly long questions (>100 words)
- Questions that test trivia instead of understanding

## Workflow Example

Let's say you want to add questions about "Function Calling in LLMs":

### Step 1: Generate Questions

```bash
/quiz-content-agent Generate 5 medium difficulty questions about function calling and tool use in LLMs for the Model Selection category
```

The agent will:
1. Research the topic if needed
2. Review existing questions for style
3. Generate 5 questions with explanations
4. Provide them in copy-paste ready format

### Step 2: Review Output

The agent provides questions like:

```python
# Add to quiz_data.py in QUIZ_DATA list

{
    "category": "Model Selection & Context Management",
    "question": "What is the primary purpose of function calling in LLMs?",
    "options": [
        "To make the model run faster",
        "To allow the model to interact with external tools and APIs",
        "To reduce token usage",
        "To improve the model's grammar"
    ],
    "correct": 1,
    "difficulty": "medium",
    "explanation": "Function calling enables LLMs to extend their capabilities by interacting with external tools, APIs, and databases, allowing them to perform actions beyond text generation."
},
```

### Step 3: Add to quiz_data.py

Copy the questions into `quiz_data.py` in the `QUIZ_DATA` list.

### Step 4: Reseed Database

```bash
python init_db.py
```

**Warning:** This drops all existing data and recreates the database!

### Step 5: Test

Start the app and test your new questions:

```bash
python app.py
```

Navigate to http://localhost:5000 and take the quiz.

## Advanced Usage

### Validate Before Adding

Before committing new questions:

```bash
/quiz-content-agent Review these new questions for quality before I add them to the database: [paste questions]
```

### Balance Your Question Bank

```bash
/quiz-content-agent Analyze distribution and tell me what questions to add to achieve better balance
```

The agent might respond:
- "Add 3 more hard questions to Agent Fundamentals"
- "Prompt Engineering has too many easy questions, add 2 hard ones"
- "Model Selection needs more questions about context window management"

### Check After Bulk Additions

After adding many questions:

```bash
/quiz-content-agent Check all questions for duplicates and quality issues
```

## Tips for Best Results

1. **Be Specific**: Instead of "generate questions", say "generate 5 medium difficulty questions about prompt chaining strategies"

2. **Provide Context**: Mention if questions should focus on practical application vs. theory

3. **Review Before Adding**: Always validate generated questions before adding to database

4. **Iterate**: If questions aren't quite right, ask the agent to revise them

5. **Check Distribution**: Periodically analyze balance to ensure comprehensive coverage

6. **Update Regularly**: As AI/ML best practices evolve, refresh outdated questions

## Common Use Cases

### Expanding a Category

```bash
/quiz-content-agent We only have 7 questions in Model Selection. Generate 5 more covering: API selection, cost optimization, and latency considerations
```

### Improving Quality

```bash
/quiz-content-agent Some of our questions feel too easy. Review all "medium" difficulty questions and identify any that should be "easy" or "hard"
```

### Creating a New Topic Module

```bash
/quiz-content-agent Create a complete module (8-10 questions across all difficulty levels) about LangChain and agent frameworks
```

### Spring Cleaning

```bash
/quiz-content-agent Review all questions, check for outdated information (remember it's 2025), duplicates, and quality issues. Provide a comprehensive report.
```

## Limitations

- Agent generates questions but **doesn't automatically add them** to the database
- You must manually copy questions to `quiz_data.py`
- Running `init_db.py` **drops all user data** (attempts, users, etc.)
- Agent follows the 3 existing categories - can't create new categories without code changes

## File Locations

- **Slash Command Definition**: `.claude/commands/quiz-content-agent.md`
- **Question Data**: `quiz_data.py` (QUIZ_DATA list)
- **Database Seed Script**: `init_db.py`
- **This Guide**: `QUIZ_CONTENT_AGENT_GUIDE.md`

## Troubleshooting

### Agent isn't available
- Make sure you're in the project directory
- Check that `.claude/commands/quiz-content-agent.md` exists
- Try `/help` to see all available commands

### Questions don't appear in app
- Did you add them to `quiz_data.py`?
- Did you run `python init_db.py`?
- Check for Python syntax errors in `quiz_data.py`

### Questions are low quality
- Provide more specific instructions to the agent
- Ask it to review and revise
- Reference existing high-quality questions as examples

## Example Session

Here's a complete example of using the Quiz Content Agent:

```bash
# Check current distribution
/quiz-content-agent Analyze question distribution

# Agent responds: You have 8/10/7 questions across categories,
# with gaps in hard difficulty for Model Selection

# Generate to fill gap
/quiz-content-agent Generate 3 hard questions about context window management and token optimization for Model Selection category

# Agent provides 3 questions in proper format

# Validate before adding
/quiz-content-agent Review these 3 questions for accuracy and appropriate difficulty

# Agent confirms quality, you copy to quiz_data.py

# Reseed database
python init_db.py

# Test in app
python app.py
```

## Next Steps

1. Try the agent: `/quiz-content-agent Analyze current question distribution`
2. Generate your first questions
3. Validate quality
4. Add to database
5. Test in the app

Happy question creation! 🎯
