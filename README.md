# Claude Code Quiz App

A Flask-based quiz application that tests your knowledge of AI software development concepts with Claude Code.

## Topics Covered

1. **CLAUDE.md** - Project context and instructions
2. **Agents** - When and how to use specialized agents
3. **Custom Commands** - Creating and using slash commands
4. **Planning Workflow** - Plan mode and implementation strategies
5. **Model Selection** - Choosing between Sonnet, Opus, and Haiku
6. **Context Management** - Managing conversation context
7. **Permissions** - Auto-approval vs. manual review
8. **Review Process** - Efficiently reviewing changes
9. **MCP** - Model Context Protocol and extensions

## Features

- 18 comprehensive questions (2 per topic)
- **Difficulty Levels**: Choose between Easy, Medium, or Hard questions
- Choose to quiz on all topics or specific topics
- **Flexible Filtering**: Combine topic and difficulty selection
- Instant feedback with explanations
- Detailed results with topic breakdown
- Review all answers with explanations
- Beautiful, responsive UI with color-coded difficulty badges
- Keyboard shortcuts for faster navigation (1-4 keys to select answers)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

1. Start the Flask development server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## How to Use

1. **Choose Quiz Mode**: Select "All Topics" for a comprehensive quiz, or pick a specific topic to focus on
2. **Choose Difficulty Level**: Select Easy, Medium, Hard, or All Levels
3. **Answer Questions**: Click on your answer choice or use keyboard shortcuts (1-4)
4. **Review Results**: See your score, topic breakdown, and detailed explanations for each question
5. **Retake**: Take the quiz again to improve your score!

## Difficulty Levels

The quiz includes three difficulty levels:

- **Easy (🟢)**: Basic concepts and definitions - 7 questions
- **Medium (🟡)**: Application of concepts and when-to-use scenarios - 7 questions
- **Hard (🔴)**: Best practices, complex scenarios, and trade-offs - 4 questions

You can filter by difficulty level alone, combine it with a specific topic, or practice all levels together!

## Project Structure

```
claude_training/
├── app.py                 # Flask application with routes
├── quiz_data.py          # Quiz questions and data
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html        # Base template with styling
│   ├── index.html       # Landing page
│   ├── question.html    # Question display
│   └── results.html     # Results and review
└── README.md            # This file
```

## Scoring

- **90%+**: Excellent! You've mastered Claude Code
- **70-89%**: Great job! Solid understanding
- **50-69%**: Good effort! Review topics you missed
- **Below 50%**: Keep learning! Review the documentation

## Tips for Success

- Read each question carefully
- Think about practical use cases
- Review the explanations even for questions you got right
- Focus on topics where you scored lower
- Practice using Claude Code in real projects

## Built With

- Flask 3.0.0
- Python 3.x
- HTML/CSS
- Responsive design

---

Built with Claude Code | AI Software Development Training
