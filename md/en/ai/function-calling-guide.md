---
title: "LLM Function Calling: Complete Developer Guide with Code Examples"
description: "How to implement function calling / tool use with OpenAI, Anthropic, and Gemini APIs. Schema design, parallel calls, error handling, and chaining multiple function calls. Working examples in Python and TypeScript."
date: 2026-05-08
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/function-calling-guide.html
---

# LLM Function Calling: Complete Developer Guide with Code Examples

Function calling (or "tool use") transforms an LLM from a chatbot into an agent that can take actions: query databases, send emails, create tickets, call APIs. Every major LLM provider now supports it, but the implementation details differ significantly. This guide covers how to design function schemas, handle errors, and implement reliable tool-use workflows across OpenAI, Anthropic, and Gemini.

## How Function Calling Works
    
    
    1. You define functions (name, description, parameters JSON Schema)
    2. User sends a message: "What is the weather in Tokyo?"
    3. LLM returns: { function: "get_weather", arguments: { city: "Tokyo" } }
    4. Your code executes get_weather("Tokyo") -> { temp: 22, condition: "sunny" }
    5. You send the function result back to the LLM
    6. LLM generates the final response: "It is currently 22C and sunny in Tokyo."

## Function Schema Design: Best Practices

Practice| Good Example| Bad Example  
---|---|---  
Descriptive names| search_customer_by_email| search (too generic, LLM confuses with other search functions)  
Clear descriptions| "Search for a customer by their email address. Returns customer ID, name, and subscription status."| "Searches for a customer" (does not tell LLM when to use it or what it returns)  
Typed parameters| "email": { "type": "string", "format": "email" }| "email": { "type": "string" } (missing format constraint)  
Enums for choices| "sort_by": { "enum": ["name", "date", "amount"] }| "sort_by": { "type": "string" } (LLM may invent values)  
Required vs optional| required: ["customer_id"], optional: ["include_archived"]| Everything required (LLM may hallucinate values for optional params)  
  
## Parallel vs Sequential Function Calls

**Parallel calls:** When two functions are independent, the LLM can call them simultaneously. "What is the weather in Tokyo AND the exchange rate for JPY?" -> 2 parallel calls. **Sequential calls:** When one function's output is needed as input to another. "Find customer by email, then get their recent orders" -> 2 sequential calls. Design your schemas so independent functions can be called in parallel — it reduces latency from 2x call time to max(call1, call2).

## Error Handling Patterns
    
    
    # Pattern 1: Return errors as structured function results
    def get_customer(email: str):
        try:
            customer = db.customers.find_by_email(email)
            if not customer:
                return {"error": "NOT_FOUND", "message": f"No customer with email {email}"}
            return {"customer": customer}
        except Exception as e:
            return {"error": "INTERNAL", "message": str(e)}
    
    # The LLM can then respond appropriately:
    # "I could not find a customer with that email address. Would you like to try a different one?"
    
    # Pattern 2: Validate arguments before execution
    # If LLM calls get_weather(city="") or missing required args, return descriptive error
    # This trains the LLM over multiple turns to provide correct arguments

## Provider-Specific Implementation

Provider| API Parameter| Key Difference  
---|---|---  
OpenAI| tools: [{type: "function", function: {...}}]| tool_choice: "auto" | "required" | "none" | specific function  
Anthropic| tools: [{name: "...", description: "...", input_schema: {...}}]| Native tool_use content blocks; can force tool use  
Google Gemini| tools: [{functionDeclarations: [{name, description, parameters}]}]| Automatic function calling mode available (Gemini executes)  
  
**Bottom line:** Function calling is the bridge between LLMs and real-world actions. Invest time in schema design (clear descriptions, typed parameters, enums) — the quality of your function definitions directly determines reliability. Start with 2-3 functions and test extensively before adding more. See also: [AI Agents Guide](</en/ai/ai-agents-guide.html>) and [AI API Integration Guide](</en/ai/ai-api-integration-guide.html>).

**See also:** [MCP (Model Context Protocol) Complete Guide: The Standard Connecting AI to Your Tools](</en/ai/mcp-complete-guide.html>), [How to Build a Custom GPT Plugin: Complete Developer Guide](</en/ai/build-chatgpt-plugin.html>), [Advanced Prompt Engineering: Techniques That Actually Work for Developers](</en/ai/prompt-engineering-advanced.html>)
