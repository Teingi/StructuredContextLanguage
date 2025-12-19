# Structured Context Language

## Overview
People are familiar with SQL (Structured Query Language), which is used to interact with databases. Today, as we face Large Language Models (LLMs), the focus is shifting from prompt engineering to context engineering.

In this repository, we aim to build a Structured Context Language (SCL) to occupy a niche analogous to SQL, drawing inspiration from context engineering practices.

We hope that through this effort, we can distill a middleware solution. This middleware would provide a standard interface for AI agents, much like Hibernate serves as a standard ORM interface for Java applications.

## Deconstructing SCL

If we consider prompts as a query language for Large Language Models (LLM), then context engineering is undoubtedly an implementation of this query language. We can deconstruct context engineering along three independent dimensions:

- Business Content: Specific instructions for particular prompts and scenarios.
- Tool Invocation: Various tools the LLM can use to obtain additional external data.
- Memory Management: In multi-turn conversation scenarios, determining which historical content is relevant to the current query.

> We can view tool invocation as a spatial expansion of information and memory management as an expansion of information along the temporal dimension.

Considering that in engineering practice, we can implement interactions for memory management through tool invocation, the extended querying of information within context engineering can therefore be accomplished using a standardized interface and further summarized into a standardized workflow.

Inspired by the progressive loading mechanism of Claude Skill, we have also observed that autonomous selection of tools by the LLM can be achieved through progressive loading across different tools. Unlike stored procedures in SQL, which are defined and explicitly called for execution, progressive loading provides an additional layer of autonomy.

## Use case
> The Autonomy Slider —— Reference Karpathy's speech on Software 3.0. Show me the diff in vivid.

```
Configurable + Autonomy by LLM via feedback control
Autonomy by LLM via feedback control(metric or history)
Autonomy by LLM
Configurable
HardCode
```

- [ ] Should we make a middleware just input as prompt and output as result?(Autonomy)
- [ ] We provides workflow and let people able to config it.(Configurable)
- [ ] We provides sdk let people implements their own.(Hardcode)

- [ ] Obversbility —— otel.

- [ ] Function selction.
   - [ ] "Progressive loading" base on RAG. (Autonomy)
   - [ ] Hard code memory tool invoke. (Autonomy or defualt? tbd)
   - [ ] Hardcode control by human, as index hint for SQL?.
   - [ ] Hardcode control by human as input.

- [ ] File format Autonomy, took PDF format as example.
    - [ ] Context auto into markdown.(Autonomy)
    - [ ] Context auto embedding for RAG.(Autonomy)
    - [ ] Or Hardcode control by human outside our process.

- [ ] Content Autonomy.
    - [ ] RAG support by default.(Autonomy)
    - [ ] Hard code as input prompt content.(Hardcode control by human)

## LLM Chat Implementation

This repository includes a flexible LLM chat implementation that supports both OpenAI and Anthropic providers with function calling capabilities:

- `llm_chat.py`: Core implementation supporting both OpenAI and Anthropic
- `example_llm_usage.py`: Examples of how to use the LLM chat functionality

### Features

- **Multi-provider support**: Works with both OpenAI and Anthropic APIs
- **Function calling**: Supports tool/function calling with OpenAI models
- **OpenTelemetry integration**: Built-in tracing for observability
- **Extensible design**: Easy to add new providers or functions

### Usage

1. Set your API keys as environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-key"
   export ANTHROPIC_API_KEY="your-anthropic-key"
   ```

2. Use in your code:
   ```python
   from llm_chat import LLMChat
   
   # Initialize with OpenAI
   llm = LLMChat(provider="openai")
   
   # Simple chat
   messages = [
       {"role": "system", "content": "You are a helpful assistant."},
       {"role": "user", "content": "Hello!"}
   ]
   response = llm.chat(messages)
   print(response["content"])
   ```

### Testing

The project includes a comprehensive test suite:

- `tests/test_llm_chat.py`: Unit tests for the LLM chat implementation
- `run_tests.py`: Test runner script

To run the tests:
```bash
python run_tests.py
```

## todo
Find some agent bench mark for testing.
