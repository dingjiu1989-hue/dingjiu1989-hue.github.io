---
title: "LLM Fine-Tuning Guide"
description: "Learn how to fine-tune LLMs effectively using LoRA, QLoRA, and full fine-tuning techniques with practical code examples."
date: 2025-12-12
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/llm-fine-tuning.html
---

# LLM Fine-Tuning Guide

## Introduction

Fine-tuning adapts a pre-trained language model to a specific task or domain. While prompt engineering and RAG handle many use cases out of the box, fine-tuning is essential when you need consistent formatting, domain-specific knowledge, or behavior that base models cannot achieve through prompting alone. This guide covers the full spectrum of fine-tuning approaches.

## When to Fine-Tune

Before investing in fine-tuning, consider whether simpler approaches suffice:

  * **Prompt engineering** : Good for simple formatting changes and basic instructions

  * **RAG** : Ideal for knowledge-intensive tasks with verifiable sources

  * **Fine-tuning** : Necessary for specialized output formats, tone adaptation, and consistent behavior patterns




Fine-tuning becomes cost-effective when you need to run many similar queries and can amortize the training cost over thousands or millions of inference calls.

## Fine-Tuning Approaches

## Full Fine-Tuning

Full fine-tuning updates all model parameters on a target dataset. This approach achieves the highest quality but requires substantial compute — full fine-tuning of a 7B parameter model requires approximately 56 GB of GPU memory per batch.

**When to use full fine-tuning:**

  * You have access to high-memory GPUs (A100 80GB or H100)

  * Your dataset is large and diverse (10,000+ examples)

  * The domain shift from pre-training data is significant

  * Maximum quality is critical




## LoRA (Low-Rank Adaptation)

LoRA injects trainable rank-decomposition matrices into the model's attention layers, reducing the number of trainable parameters by 10,000x. A 7B model can be fine-tuned with LoRA on a single consumer GPU with 24 GB memory.

from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(

r=16, # Rank of the update matrices

lora_alpha=32, # Scaling factor

target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],

lora_dropout=0.05,

bias="none",

task_type="CAUSAL_LM"

)

model = get_peft_model(base_model, lora_config)

print(f"Trainable params: {model.num_parameters(only_trainable=True):,}")

## Output for Llama 2 7B: ~4,194,304 params (0.06% of total)

**Key hyperparameters:**

  * **r (rank)** : Higher values (16-64) for complex tasks, lower (4-8) for simpler formatting. Rank 16 works well for most use cases

  * **alpha** : Typically double the rank value (alpha = 2 * r)

  * **Target modules** : Include all attention projection matrices for best results




## QLoRA (Quantized LoRA)

QLoRA combines 4-bit quantization with LoRA, enabling fine-tuning of 65B models on a single 48GB GPU. The model weights are quantized to 4-bit while LoRA adapters remain in full precision.

from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(

load_in_4bit=True,

bnb_4bit_use_double_quant=True,

bnb_4bit_quant_type="nf4",

bnb_4bit_compute_dtype=torch.bfloat16

)

model = AutoModelForCausalLM.from_pretrained(

"meta-llama/Llama-2-7b-hf",

quantization_config=bnb_config,

device_map="auto"

)

QLoRA achieves approximately 99% of full fine-tuning performance while reducing memory requirements by 4x.

## Dataset Preparation

Dataset quality matters more than quantity. A well-curated 1,000-example dataset outperforms a noisy 10,000-example one.

**Guidelines for instruction tuning datasets:**

  * **Diverse prompts** : Cover all edge cases your system will encounter



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Correct responses** : Each response must be factually accurate and follow the desired format

3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Consistent formatting** : Use the same chat template throughout

4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Balanced distribution** : Avoid over-representing common patterns

5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Validation split** : Hold out 5-10% for evaluation

**Format example:**

{

"instruction": "Summarize the following meeting notes in 2-3 bullet points.",

"input": "Team discussed Q1 results. Revenue grew 15%. Engineering shipped 3 features. Marketing launched new campaign.",

"output": "- Q1 revenue grew 15%\n- Engineering shipped 3 new features\n- Marketing launched a new campaign"

}

## Training Process

Modern fine-tuning uses the SFT (Supervised Fine-Tuning) trainer:

from trl import SFTTrainer

trainer = SFTTrainer(

model=model,

train_dataset=train_dataset,

eval_dataset=eval_dataset,

dataset_text_field="text",

max_seq_length=2048,

args=TrainingArguments(

per_device_train_batch_size=4,

gradient_accumulation_steps=4,

learning_rate=2e-4,

num_train_epochs=3,

logging_steps=10,

save_strategy="epoch",

)

)

trainer.train()

## Evaluation

Evaluate fine-tuned models on:

  * **Task accuracy** : Does the model produce correct outputs?

  * **Format compliance** : Does it follow the required structure?

  * **Hallucination rate** : Does it invent facts?

  * **Regression** : Has performance degraded on unrelated tasks?




Use an automated evaluation harness comparing the fine-tuned model against the base model on a held-out test set.

## Conclusion

Fine-tuning remains the most powerful tool for adapting LLMs to specific domains and tasks. Start with QLoRA for cost-effective experimentation, scale to full fine-tuning only when quality demands it. Focus on dataset quality over quantity, and always measure performance against a clear baseline.

**See also:** [Fine-Tuning Open Source LLMs: A Developer's Practical Guide (2026)](</en/ai/fine-tune-open-source-llm.html>), [AI Code Generation Best Practices](</en/ai/ai-code-generation.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>).

**See also:** [Fine-Tuning Open Source LLMs: A Developer's Practical Guide (2026)](</en/ai/fine-tune-open-source-llm.html>), [Running LLMs Locally](</en/ai/local-llm-setup.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [Fine-Tuning Open Source LLMs: A Developer's Practical Guide (2026)](</en/ai/fine-tune-open-source-llm.html>), [Running LLMs Locally](</en/ai/local-llm-setup.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [Fine-Tuning Open Source LLMs: A Developer's Practical Guide (2026)](</en/ai/fine-tune-open-source-llm.html>), [Running LLMs Locally](</en/ai/local-llm-setup.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [Fine-Tuning Open Source LLMs: A Developer's Practical Guide (2026)](</en/ai/fine-tune-open-source-llm.html>), [Running LLMs Locally](</en/ai/local-llm-setup.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [Fine-Tuning Open Source LLMs: A Developer's Practical Guide (2026)](</en/ai/fine-tune-open-source-llm.html>), [Running LLMs Locally](</en/ai/local-llm-setup.html>), [LLM Fine-Tuning Strategies and Techniques](</en/ai/fine-tuning-strategies.html>)

**See also:** [Advanced Prompt Engineering Techniques](</en/ai/ai-prompt-engineering.html>), [LLM Context Window Management](</en/ai/llm-context-window.html>), [Deploying AI Agents to Production](</en/ai/ai-agents-production.html>)

**See also:** [Advanced Prompt Engineering Techniques](</en/ai/ai-prompt-engineering.html>), [LLM Context Window Management](</en/ai/llm-context-window.html>), [Deploying AI Agents to Production](</en/ai/ai-agents-production.html>)

**See also:** [Advanced Prompt Engineering Techniques](</en/ai/ai-prompt-engineering.html>), [LLM Context Window Management](</en/ai/llm-context-window.html>), [Deploying AI Agents to Production](</en/ai/ai-agents-production.html>)

**See also:** [Advanced Prompt Engineering Techniques](</en/ai/ai-prompt-engineering.html>), [LLM Context Window Management](</en/ai/llm-context-window.html>), [Deploying AI Agents to Production](</en/ai/ai-agents-production.html>)

**See also:** [Advanced Prompt Engineering Techniques](</en/ai/ai-prompt-engineering.html>), [LLM Context Window Management](</en/ai/llm-context-window.html>), [Deploying AI Agents to Production](</en/ai/ai-agents-production.html>)

**See also:** [Advanced Prompt Engineering Techniques](</en/ai/ai-prompt-engineering.html>), [LLM Context Window Management](</en/ai/llm-context-window.html>), [Deploying AI Agents to Production](</en/ai/ai-agents-production.html>)

**See also:** [Advanced Prompt Engineering Techniques](</en/ai/ai-prompt-engineering.html>), [LLM Context Window Management](</en/ai/llm-context-window.html>), [Deploying AI Agents to Production](</en/ai/ai-agents-production.html>)

**See also:** [Advanced Prompt Engineering Techniques](</en/ai/ai-prompt-engineering.html>), [LLM Context Window Management](</en/ai/llm-context-window.html>), [Deploying AI Agents to Production](</en/ai/ai-agents-production.html>)
