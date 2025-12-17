# Database Agent Guide

Quick reference for using the `/database-agent` slash command.

## What is the Database Agent?

A specialized AI agent that focuses on database architecture, optimization, and data management for the Flask Quiz App. It handles schema design, query optimization, migrations, indexing, and data integrity.

## How to Use

```bash
/database-agent [task description]
```

## Common Use Cases

### 1. Performance Optimization
```bash
/database-agent Optimize database queries and add indexes
/database-agent Fix the N+1 query problem on the dashboard
/database-agent Analyze and improve query performance
```

### 2. Schema Improvements
```bash
/database-agent Add data validation constraints to models
/database-agent Review schema and suggest improvements
/database-agent Add check constraints to ensure data integrity
```

### 3. Database Migration
```bash
/database-agent Help me migrate from SQLite to PostgreSQL
/database-agent Set up Flask-Migrate for schema versioning
/database-agent Create migration strategy for production
```

### 4. New Features
```bash
/database-agent Design a bookmarks table for saving questions
/database-agent Add a leaderboard table with proper indexes
/database-agent Design schema for timed quiz tracking
```

### 5. Query Analysis
```bash
/database-agent Analyze queries in app.py and find bottlenecks
/database-agent Add eager loading to prevent N+1 problems
/database-agent Review and optimize the dashboard queries
```

## What the Database Agent Can Do

### Schema Design
- ✅ Analyze existing database schema
- ✅ Identify missing indexes and constraints
- ✅ Design new tables with proper relationships
- ✅ Add check constraints for data validation
- ✅ Implement unique constraints
- ✅ Define cascade behaviors

### Query Optimization
- ✅ Identify N+1 query problems
- ✅ Add eager loading with `joinedload()`
- ✅ Create composite indexes
- ✅ Optimize JOIN operations
- ✅ Add query result caching
- ✅ Implement pagination

### Migrations
- ✅ Migrate from SQLite to PostgreSQL
- ✅ Set up Flask-Migrate
- ✅ Create migration scripts
- ✅ Handle data type conversions
- ✅ Plan production deployment

### Data Integrity
- ✅ Add foreign key constraints
- ✅ Implement check constraints
- ✅ Define unique constraints
- ✅ Set up proper cascades
- ✅ Transaction management

### Performance Monitoring
- ✅ Log slow queries
- ✅ Analyze query plans
- ✅ Index recommendations
- ✅ Caching strategies

## Current Schema Overview

```
users (N)
├── id, username, created_at, last_active
└── attempts (1:N)

quizzes (3)
├── id, category, title, description, icon, created_at
├── questions (1:N)
└── attempts (1:N)

questions (40)
├── id, quiz_id, question_text, options, correct_answer
├── explanation, difficulty, order_index
└── user_answers (1:N)

attempts (N)
├── id, user_id, quiz_id, started_at, completed_at
├── score, total_questions, percentage
└── user_answers (1:N)

user_answers (N)
├── id, attempt_id, question_id, selected_answer
└── is_correct, answered_at
```

## Known Issues the Agent Can Fix

### Missing Indexes
- `users.username` - frequent login lookups
- `users.last_active` - dashboard sorting
- `quizzes.category` - category filtering
- `questions.quiz_id` - foreign key lookups
- `questions.difficulty` - difficulty filtering
- `attempts.(user_id, quiz_id)` - composite index
- `attempts.completed_at` - filtering completed
- `user_answers.attempt_id` - answer reviews
- `user_answers.question_id` - question analytics

### Missing Constraints
- `quizzes.category` - should be unique
- `questions.correct_answer` - should be 0-3
- `questions.difficulty` - should be enum
- `attempts.score` - should be <= total_questions
- `attempts.percentage` - should be 0-100
- `user_answers.(attempt_id, question_id)` - unique pair
- `user_answers.selected_answer` - should be 0-3 or NULL

### N+1 Query Problems
- Dashboard loading attempts with quiz info
- History page loading all attempts
- Results page loading question details

## Example Workflows

### Optimize Existing Database
```bash
# Step 1: Analyze current performance
/database-agent Analyze database performance and identify issues

# Step 2: Add indexes
/database-agent Add recommended indexes to all models

# Step 3: Fix N+1 problems
/database-agent Fix N+1 query problems in dashboard route

# Step 4: Add constraints
/database-agent Add check constraints for data validation
```

### Migrate to PostgreSQL
```bash
# Step 1: Assessment
/database-agent Assess SQLite to PostgreSQL migration requirements

# Step 2: Setup
/database-agent Set up Flask-Migrate and configure PostgreSQL

# Step 3: Migration
/database-agent Create initial migration and test locally

# Step 4: Deployment
/database-agent Provide production deployment instructions
```

### Add New Feature
```bash
# Example: Bookmarking questions
/database-agent Design a bookmarks table for users to save questions

# The agent will:
# 1. Design schema with user_id and question_id
# 2. Add proper indexes and constraints
# 3. Create the model in models.py
# 4. Set up relationships
# 5. Provide migration script
# 6. Suggest API integration
```

## Best Practices

The Database Agent follows these principles:

✅ **Performance First**
- Always add indexes on foreign keys
- Use composite indexes for multi-column queries
- Eager load relationships to prevent N+1
- Paginate large result sets

✅ **Data Integrity**
- Add check constraints for validation
- Use unique constraints to prevent duplicates
- Define proper cascade behavior
- Wrap related operations in transactions

✅ **Maintainability**
- Use Flask-Migrate for schema versioning
- Document schema changes
- Keep migrations reversible
- Test migrations before production

❌ **Avoid**
- Too many indexes (slows writes)
- Missing foreign key indexes
- Ignoring N+1 problems
- Hardcoding SQL strings
- Missing error handling

## Quick Commands Reference

| Task | Command |
|------|---------|
| Add indexes | `/database-agent Add indexes to improve query performance` |
| Fix N+1 | `/database-agent Fix N+1 query problems` |
| Add constraints | `/database-agent Add data validation constraints` |
| Migrate to PostgreSQL | `/database-agent Set up PostgreSQL migration` |
| Design new table | `/database-agent Design [feature] table` |
| Analyze queries | `/database-agent Analyze and optimize queries` |
| Review schema | `/database-agent Review schema and suggest improvements` |

## Integration with Other Agents

The Database Agent works well with:

- **Backend Agent** (`/backend-agent`) - Implements features that need database changes
- **Quiz Content Agent** (`/quiz-content-agent`) - Adds questions that get stored in database

## Files Modified by Database Agent

- `models.py` - Primary focus (models, indexes, constraints)
- `init_db.py` - Seeding and initialization
- `app.py` - Query optimization
- `requirements.txt` - Add psycopg2, Flask-Migrate
- `config.py` - Database configuration (may create)

## Resources

**SQLAlchemy Documentation:**
- https://docs.sqlalchemy.org/
- https://flask-sqlalchemy.palletsprojects.com/

**Flask-Migrate:**
- https://flask-migrate.readthedocs.io/

**PostgreSQL:**
- https://www.postgresql.org/docs/

---

**Pro Tip**: Run `/database-agent Review current schema and suggest optimizations` to get a comprehensive analysis of your database setup!
