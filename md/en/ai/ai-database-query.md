---
title: "Natural Language to SQL with LLMs"
description: "Build systems that convert natural language questions into SQL queries using LLMs, with schema context, query validation, and safety guards."
date: 2026-05-11
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/ai-database-query.html
---

# Natural Language to SQL with LLMs

# Natural Language to SQL with LLMs

# Natural Language to SQL with LLMs

# Natural Language to SQL with LLMs

# Natural Language to SQL with LLMs

# Natural Language to SQL with LLMs

# Natural Language to SQL with LLMs

# Natural Language to SQL with LLMs

# Natural Language to SQL with LLMs

# Natural Language to SQL with LLMs

# Natural Language to SQL with LLMs

# Natural Language to SQL with LLMs

# Natural Language to SQL with LLMs

## Introduction

Natural language to SQL (NL2SQL) is one of the most impactful applications of LLMs in data analytics. It enables non-technical users to query databases using plain English, democratizing data access across organizations. While early NL2SQL systems were fragile, modern LLMs can generate accurate SQL for complex analytical queries — when properly configured with schema context, safety guards, and validation.

## How NL2SQL Works

The core architecture is straightforward:

User Question → Context Assembly → LLM SQL Generation → Query Validation → Execution → Result Formatting

The critical step is **context assembly** — providing the LLM with enough database metadata to generate correct SQL.

## Schema Context

The LLM needs to understand your database schema. A well-structured schema prompt includes:

CREATE TABLE customers (

customer_id INTEGER PRIMARY KEY,

first_name VARCHAR(100),

last_name VARCHAR(100),

email VARCHAR(255),

signup_date DATE,

country VARCHAR(50),

lifetime_value DECIMAL(10,2)

);

CREATE TABLE orders (

order_id INTEGER PRIMARY KEY,

customer_id INTEGER REFERENCES customers(customer_id),

order_date TIMESTAMP,

total_amount DECIMAL(10,2),

status VARCHAR(20) -- pending, shipped, delivered, cancelled

);

CREATE TABLE order_items (

item_id INTEGER PRIMARY KEY,

order_id INTEGER REFERENCES orders(order_id),

product_name VARCHAR(200),

quantity INTEGER,

unit_price DECIMAL(10,2)

);

**Key additions for better accuracy:**

  * Column descriptions: `-- customer's two-letter ISO country code`

  * Value examples: `-- status options: pending, shipped, delivered, cancelled`

  * Relationship hints: `-- join via customer_id to get customer details`

  * Index hints: `-- indexed on order_date for range queries`




def build_schema_context(tables):

context_parts = []

for table in tables:

ddl = f"CREATE TABLE {table.name} (\n"

for col in table.columns:

ddl += f" {col.name} {col.type} -- {col.description}\n"

ddl += ");"

context_parts.append(ddl)

# Add sample rows for context on data patterns

if table.sample_rows:

context_parts.append(f"-- Sample row: {table.sample_rows[0]}")

return "\n\n".join(context_parts)

## Few-Shot Examples

For complex schemas, provide question-SQL pairs relevant to the query:

few_shot_examples = [

{

"question": "Show me the top 5 customers by total spending",

"query": """

SELECT

c.first_name || ' ' || c.last_name AS customer_name,

SUM(o.total_amount) AS total_spent

FROM customers c

JOIN orders o ON c.customer_id = o.customer_id

WHERE o.status != 'cancelled'

GROUP BY c.customer_id, c.first_name, c.last_name

ORDER BY total_spent DESC

LIMIT 5

"""

},

{

"question": "What was the monthly revenue for 2025?",

"query": """

SELECT

DATE_TRUNC('month', o.order_date) AS month,

SUM(o.total_amount) AS revenue

FROM orders o

WHERE o.status = 'delivered'

AND o.order_date >= '2025-01-01'

AND o.order_date < '2026-01-01'

GROUP BY month

ORDER BY month

"""

}

]

**Dynamic example retrieval** using embedding similarity improves accuracy significantly. Store question-query pairs in a vector database and retrieve the most relevant ones for each new question.

## SQL Generation Prompt

The complete prompt combines schema, examples, and safety instructions:

def build_nl2sql_prompt(question, schema, examples, dialect="postgresql"):

prompt = f"""You are a {dialect} SQL expert. Convert natural language questions into SQL queries.

Database Schema:

{schema}

Rules:

1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Return ONLY the SQL query, no explanations

2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Use proper JOINs based on foreign key relationships

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Handle NULLs appropriately with COALESCE or IS NULL checks

4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Use appropriate aggregate functions (COUNT, SUM, AVG) when needed

5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Always include filters to exclude irrelevant data

6\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Use LIMIT for result size control

7\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Order results when ordering is implied

8\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Never use DELETE, UPDATE, INSERT, DROP, or ALTER statements

Examples:

"""

for ex in examples:

prompt += f"\nQ: {ex['question']}\nSQL: {ex['query']}\n"

prompt += f"\nQ: {question}\nSQL:"

return prompt

## Query Validation

Before executing generated SQL, validate it:

def validate_sql(query, allowed_tables):

errors = []

# Safety check: no mutations

forbidden_keywords = ["DELETE", "UPDATE", "INSERT", "DROP", "ALTER", "TRUNCATE", "CREATE"]

for keyword in forbidden_keywords:

if keyword in query.upper():

errors.append(f"Forbidden operation: {keyword}")

# Check table references

parsed = sqlparse.parse(query)[0]

used_tables = extract_tables(parsed)

for table in used_tables:

if table not in allowed_tables:

errors.append(f"Unauthorized table: {table}")

# Syntax validation

try:

conn = get_dummy_connection(dialect)

conn.execute(f"EXPLAIN {query}")

except Exception as e:

errors.append(f"SQL syntax error: {str(e)}")

return errors

## Advanced Techniques

### Self-Correction Loop

When the generated SQL fails or returns empty results, the system can self-correct:

def nl2sql_with_correction(question, schema, max_attempts=3):

for attempt in range(max_attempts):

query = generate_sql(question, schema)

errors = validate_sql(query)

if not errors:

try:

results = execute_sql(query)

if results:

return format_results(question, query, results)

else:

feedback = "The query returned no results. Try a broader search."

except Exception as e:

feedback = f"Execution error: {str(e)}"

else:

feedback = f"Validation errors: {', '.join(errors)}"

question = f"Original question: {question}\nPrevious attempt failed: {feedback}\nPlease fix the SQL query."

### Schema Linking

For large schemas with many tables, first identify relevant tables before generating SQL:

def identify_relevant_tables(question, all_tables, table_descriptions):

prompt = f"""

Question: {question}

Available tables with descriptions:

{table_descriptions}

List only the tables needed to answer this question, comma-separated:

"""

response = call_llm(prompt)

return [t.strip() for t in response.split(",")]

This dramatically reduces context size and improves accuracy on large databases.

## Production Deployment

**Security** : Always use a read-only database user, set statement timeouts, and implement rate limiting per user.

**Caching** : Cache common NL2SQL conversions to reduce LLM costs, but invalidate when schema changes.

**Monitoring** : Log all generated queries and user feedback. Track query success rate, execution time, and correction frequency.

**User experience** : Show the generated SQL to users (with a "view query" option), and allow them to provide feedback on results.

## Conclusion

Natural language to SQL with LLMs is production-ready for analytical queries. The key success factors are high-quality schema context, relevant few-shot examples, robust query validation, and a self-correction loop. Start with a limited set of tables, measure query accuracy, and expand as you gain confidence. This technology is transforming data access, making self-serve analytics a reality for non-technical team members.

**See also:** [Running LLMs Locally](</en/ai/local-llm-setup.html>), [LLM Fine-Tuning Guide](</en/ai/llm-fine-tuning.html>), [AI Code Generation Best Practices](</en/ai/ai-code-generation.html>).

**See also:** [LLM Fine-Tuning Guide](</en/ai/llm-fine-tuning.html>), [Running LLMs Locally](</en/ai/local-llm-setup.html>), [Responsible AI Development Practices](</en/ai/responsible-ai.html>)
