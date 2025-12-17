# Quiz questions covering AI software development concepts

QUIZ_DATA = [
    # Category 1: Agent Fundamentals (8 questions)
    {
        "category": "Agent Fundamentals",
        "question": "What is an AI agent?",
        "options": [
            "A software program that takes actions autonomously to achieve goals",
            "A database management system",
            "A web server",
            "A text editor"
        ],
        "correct": 0,
        "difficulty": "easy",
        "explanation": "An AI agent is a software entity that perceives its environment through sensors and acts upon it through actuators to achieve specific goals autonomously."
    },
    {
        "category": "Agent Fundamentals",
        "question": "Which component is NOT typically part of an AI agent?",
        "options": [
            "Perception (input processing)",
            "Action (output generation)",
            "Graphics rendering engine",
            "Decision-making logic"
        ],
        "correct": 2,
        "difficulty": "easy",
        "explanation": "AI agents typically consist of perception, reasoning/decision-making, and action components. Graphics rendering is unrelated to core agent functionality."
    },
    {
        "category": "Agent Fundamentals",
        "question": "When should you use a specialized agent over a general-purpose LLM?",
        "options": [
            "For simple one-shot tasks",
            "For complex multi-step workflows requiring state management",
            "Never, general-purpose LLMs are always better",
            "Only for mathematical calculations"
        ],
        "correct": 1,
        "difficulty": "medium",
        "explanation": "Specialized agents excel at complex workflows that require maintaining state, multiple tool calls, and coordinating actions over time."
    },
    {
        "category": "Agent Fundamentals",
        "question": "What is the main advantage of ReAct (Reasoning + Acting) pattern in agents?",
        "options": [
            "It's faster than other approaches",
            "It interleaves reasoning steps with actions for better decision-making",
            "It requires less memory",
            "It works without an LLM"
        ],
        "correct": 1,
        "difficulty": "medium",
        "explanation": "ReAct combines reasoning (\"I need to...\") with actions (\"Let me search...\"), allowing the agent to think through problems step-by-step while executing actions."
    },
    {
        "category": "Agent Fundamentals",
        "question": "What is agent 'memory' used for?",
        "options": [
            "Storing user passwords",
            "Caching previous interactions and learned information across sessions",
            "Reducing API costs",
            "Faster computation"
        ],
        "correct": 1,
        "difficulty": "medium",
        "explanation": "Agent memory stores conversation history, user preferences, and learned patterns, enabling continuity and personalization across sessions."
    },
    {
        "category": "Agent Fundamentals",
        "question": "What is the 'tool use' capability in AI agents?",
        "options": [
            "Ability to write code only",
            "Ability to call external APIs, databases, and functions to extend capabilities",
            "Ability to modify its own code",
            "Ability to train other models"
        ],
        "correct": 1,
        "difficulty": "hard",
        "explanation": "Tool use (function calling) allows agents to interact with external systems like APIs, databases, calculators, and code executors, vastly expanding their capabilities beyond text generation."
    },
    {
        "category": "Agent Fundamentals",
        "question": "How do you prevent infinite loops in autonomous agents?",
        "options": [
            "By setting maximum iteration limits and defining clear termination conditions",
            "By using faster hardware",
            "By reducing model temperature",
            "Infinite loops are not a concern"
        ],
        "correct": 0,
        "difficulty": "hard",
        "explanation": "Autonomous agents need safeguards like max iterations, timeout limits, and clear success/failure conditions to prevent endless execution loops."
    },
    {
        "category": "Agent Fundamentals",
        "question": "What is the main challenge with multi-agent systems?",
        "options": [
            "Higher computational cost",
            "Coordinating communication and avoiding conflicting actions between agents",
            "They require more data",
            "They cannot work with LLMs"
        ],
        "correct": 1,
        "difficulty": "hard",
        "explanation": "Multi-agent systems must handle agent coordination, communication protocols, conflict resolution, and ensuring agents work toward common goals without interference."
    },

    # Category 2: Prompt Engineering (10 questions)
    {
        "category": "Prompt Engineering",
        "question": "What is a prompt in the context of AI?",
        "options": [
            "A notification message",
            "An input instruction that guides the AI's response",
            "A database query",
            "An error message"
        ],
        "correct": 1,
        "difficulty": "easy",
        "explanation": "A prompt is the input text or instruction given to an AI model that guides what kind of response it should generate."
    },
    {
        "category": "Prompt Engineering",
        "question": "Which prompt is more likely to get a useful response?",
        "options": [
            "Write code",
            "Write a Python function that calculates the factorial of a number with error handling",
            "Do something",
            "Help"
        ],
        "correct": 1,
        "difficulty": "easy",
        "explanation": "Specific, detailed prompts with clear requirements yield better results than vague requests."
    },
    {
        "category": "Prompt Engineering",
        "question": "What is 'few-shot prompting'?",
        "options": [
            "Using very short prompts",
            "Providing a few examples in the prompt to guide the model's behavior",
            "Sending multiple prompts at once",
            "Limiting model responses to a few words"
        ],
        "correct": 1,
        "difficulty": "medium",
        "explanation": "Few-shot prompting includes examples in the prompt (e.g., \"Input: X → Output: Y\") to show the model the desired pattern or format."
    },
    {
        "category": "Prompt Engineering",
        "question": "What is the purpose of 'system prompts'?",
        "options": [
            "To restart the system",
            "To set the AI's role, behavior, and constraints for the entire conversation",
            "To fix errors",
            "To speed up responses"
        ],
        "correct": 1,
        "difficulty": "medium",
        "explanation": "System prompts establish the AI's persona, expertise domain, tone, and operational guidelines that persist across the conversation."
    },
    {
        "category": "Prompt Engineering",
        "question": "What is 'chain-of-thought' prompting?",
        "options": [
            "Asking multiple unrelated questions",
            "Asking the AI to explain its reasoning step-by-step before giving an answer",
            "Creating a blockchain",
            "Linking multiple AI models"
        ],
        "correct": 1,
        "difficulty": "medium",
        "explanation": "Chain-of-thought prompting asks the model to \"think step-by-step\" or \"explain your reasoning,\" which improves accuracy on complex problems."
    },
    {
        "category": "Prompt Engineering",
        "question": "How can you reduce hallucinations in AI responses?",
        "options": [
            "Ask for higher creativity",
            "Request citations, use specific constraints, and verify against ground truth",
            "Use shorter prompts",
            "Increase temperature"
        ],
        "correct": 1,
        "difficulty": "medium",
        "explanation": "Hallucinations can be reduced by asking for citations, providing specific factual constraints, using retrieval-augmented generation, and lower temperature settings."
    },
    {
        "category": "Prompt Engineering",
        "question": "What is 'prompt injection' and why is it a security concern?",
        "options": [
            "A way to speed up responses",
            "A vulnerability where malicious users insert instructions that override the intended prompt",
            "A technique to improve accuracy",
            "A method to reduce costs"
        ],
        "correct": 1,
        "difficulty": "hard",
        "explanation": "Prompt injection is when untrusted user input contains instructions that subvert the system prompt, potentially causing the AI to leak data or perform unintended actions."
    },
    {
        "category": "Prompt Engineering",
        "question": "What is the trade-off between 'temperature' and prompt reliability?",
        "options": [
            "There is no trade-off",
            "Higher temperature increases creativity but reduces consistency and predictability",
            "Temperature only affects speed",
            "Temperature only affects cost"
        ],
        "correct": 1,
        "difficulty": "hard",
        "explanation": "Temperature controls randomness: low (0-0.3) for consistent, deterministic outputs; high (0.7-1.0) for creative, varied responses with less predictability."
    },
    {
        "category": "Prompt Engineering",
        "question": "What is 'retrieval-augmented generation' (RAG)?",
        "options": [
            "A type of neural network",
            "Combining retrieval from a knowledge base with AI generation to ground responses in facts",
            "A prompt template",
            "A model training technique"
        ],
        "correct": 1,
        "difficulty": "hard",
        "explanation": "RAG retrieves relevant documents from a knowledge base first, then includes them in the prompt context, allowing the AI to generate responses grounded in specific factual information."
    },
    {
        "category": "Prompt Engineering",
        "question": "How do you handle prompts that exceed the model's context window?",
        "options": [
            "Just truncate the prompt",
            "Use summarization, chunking, or external memory systems to manage long contexts",
            "Increase model temperature",
            "Context limits don't matter"
        ],
        "correct": 1,
        "difficulty": "hard",
        "explanation": "For long contexts, use techniques like summarizing previous content, splitting into chunks, using external vector databases, or models with larger context windows."
    },

    # Category 3: Model Selection & Context Management (7 questions)
    {
        "category": "Model Selection & Context Management",
        "question": "What factors should you consider when choosing an AI model?",
        "options": [
            "Task complexity, latency requirements, and cost",
            "Only the model name",
            "Only the cost",
            "It doesn't matter"
        ],
        "correct": 0,
        "difficulty": "easy",
        "explanation": "Model selection depends on task complexity (simple vs. reasoning-heavy), latency needs (real-time vs. batch), cost constraints, and accuracy requirements."
    },
    {
        "category": "Model Selection & Context Management",
        "question": "What is a 'context window' in LLMs?",
        "options": [
            "A GUI element",
            "The maximum amount of text (tokens) the model can process at once",
            "A time delay",
            "A type of neural network layer"
        ],
        "correct": 1,
        "difficulty": "easy",
        "explanation": "The context window is the maximum number of tokens (input + output) the model can process in a single request."
    },
    {
        "category": "Model Selection & Context Management",
        "question": "When should you use a smaller, faster model like Claude Haiku?",
        "options": [
            "For complex reasoning and analysis",
            "For quick, straightforward tasks where speed and cost matter more than depth",
            "Never, always use the largest model",
            "Only for image processing"
        ],
        "correct": 1,
        "difficulty": "medium",
        "explanation": "Smaller models excel at simple tasks (classification, extraction, simple Q&A) where low latency and cost are priorities."
    },
    {
        "category": "Model Selection & Context Management",
        "question": "What happens when your prompt exceeds the context window?",
        "options": [
            "The model automatically compresses it",
            "The request fails or gets truncated, losing information",
            "The cost doubles",
            "Nothing, context limits are not enforced"
        ],
        "correct": 1,
        "difficulty": "medium",
        "explanation": "Exceeding context limits typically causes errors or automatic truncation, potentially losing critical information from the prompt or conversation history."
    },
    {
        "category": "Model Selection & Context Management",
        "question": "What is 'token counting' and why is it important?",
        "options": [
            "Counting database records",
            "Measuring input/output length to estimate costs and manage context limits",
            "Counting user sessions",
            "A security feature"
        ],
        "correct": 1,
        "difficulty": "medium",
        "explanation": "Token counting measures the length of text in tokens (roughly 0.75 words each), crucial for estimating API costs and staying within context limits."
    },
    {
        "category": "Model Selection & Context Management",
        "question": "What strategy should you use for a task requiring both speed and complex reasoning?",
        "options": [
            "Always use the fastest model",
            "Always use the most powerful model",
            "Use a routing approach: fast model for simple parts, powerful model for complex reasoning",
            "Split into multiple sessions"
        ],
        "correct": 2,
        "difficulty": "hard",
        "explanation": "Intelligent routing uses fast models for straightforward tasks (classification, extraction) and reserves powerful models for complex reasoning, optimizing cost and latency."
    },
    {
        "category": "Model Selection & Context Management",
        "question": "How do you manage context for a long conversation spanning hours?",
        "options": [
            "Keep all conversation history in context",
            "Use rolling summarization, storing key facts while pruning less relevant history",
            "Start a new conversation every few minutes",
            "Context management is automatic"
        ],
        "correct": 1,
        "difficulty": "hard",
        "explanation": "For long conversations, use techniques like sliding window (keep recent N messages), summarization (compress older messages), and extracting key facts to external memory."
    },
]

def get_all_topics():
    """Get list of all unique categories (kept for backwards compatibility)"""
    return list(set(q.get("category", q.get("topic", "General")) for q in QUIZ_DATA))

def get_all_categories():
    """Get list of all unique categories"""
    return list(set(q.get("category", "General") for q in QUIZ_DATA))

def get_questions_by_topic(topic):
    """Get all questions for a specific category (kept for backwards compatibility)"""
    return [q for q in QUIZ_DATA if q.get("category", q.get("topic")) == topic]

def get_questions_by_category(category):
    """Get all questions for a specific category"""
    return [q for q in QUIZ_DATA if q.get("category") == category]

def get_total_questions():
    """Get total number of questions"""
    return len(QUIZ_DATA)

def get_all_difficulties():
    """Get list of all unique difficulty levels"""
    return ["easy", "medium", "hard"]

def get_questions_by_difficulty(difficulty):
    """Get all questions for a specific difficulty level"""
    return [q for q in QUIZ_DATA if q.get("difficulty") == difficulty]

def get_questions_by_topic_and_difficulty(topic, difficulty):
    """Get questions filtered by both category and difficulty (kept for backwards compatibility)"""
    return [q for q in QUIZ_DATA
            if q.get("category", q.get("topic")) == topic and q.get("difficulty") == difficulty]

def get_questions_by_category_and_difficulty(category, difficulty):
    """Get questions filtered by both category and difficulty"""
    return [q for q in QUIZ_DATA
            if q.get("category") == category and q.get("difficulty") == difficulty]

def get_difficulty_stats():
    """Get count of questions for each difficulty level"""
    stats = {"easy": 0, "medium": 0, "hard": 0}
    for question in QUIZ_DATA:
        difficulty = question.get("difficulty", "unknown")
        if difficulty in stats:
            stats[difficulty] += 1
    return stats

def get_category_stats():
    """Get count of questions for each category"""
    stats = {}
    for question in QUIZ_DATA:
        category = question.get("category", "General")
        stats[category] = stats.get(category, 0) + 1
    return stats
