# Quickstart Guide

Get up and running with `flujo` in 5 minutes!

## 1. Install the Package

```bash
pip install flujo
```

## 2. Set Up Your API Keys

Create a `.env` file in your project directory:

```bash
cp .env.example .env
```

Add your API keys to `.env`:
```env
OPENAI_API_KEY=your_key_here
# Optional: Add other provider keys as needed
# ANTHROPIC_API_KEY=your_key_here
# GOOGLE_API_KEY=your_key_here
```

## 3. Your First Orchestration

Create a new file `hello_orchestrator.py`:

```python
from flujo.recipes import Default
from flujo import (
    Task,
    review_agent, solution_agent, validator_agent, reflection_agent,
    init_telemetry,
)

init_telemetry()

# Assemble the orchestrator with the default agents. It runs a fixed
# Review -> Solution -> Validate -> Reflection workflow.
flujo = Default(
    review_agent=review_agent,
    solution_agent=solution_agent,
    validator_agent=validator_agent,
    reflection_agent=reflection_agent,
)

task = Task(prompt="Write a haiku about programming")

best_candidate = flujo.run_sync(task)

if best_candidate:
    print("\n🎉 Best result:")
    print("-" * 40)
    print(f"Solution:\n{best_candidate.solution}")
    if best_candidate.checklist:
        print("\nQuality Checklist:")
        for item in best_candidate.checklist.items:
            status = "✅" if item.passed else "❌"
            print(f"{status} {item.description}")
```

The `Default` recipe provides a quick way to run this standard
multi-agent workflow. For custom pipelines and advanced control, you'll
use the `Flujo` engine and `Step` DSL described later.

## 4. Run Your First Orchestration

```bash
python hello_orchestrator.py
```

## 5. Try the CLI

The package includes a command-line interface for quick tasks:

```bash
# Solve a simple task
flujo solve "Write a function to calculate fibonacci numbers"

# Show your current configuration
flujo show-config

# Run a quick benchmark
flujo bench "Write a hello world program" --rounds 3

# Check version
flujo version-cmd

# Explain a pipeline structure
flujo explain path/to/pipeline.py

# Generate improvement suggestions
flujo improve path/to/pipeline.py path/to/dataset.py

# Add evaluation case (interactive)
flujo add-eval-case --dataset path/to/dataset.py
```

## 6. Next Steps

Now that you've got the basics working, you can:

1. Read the [Tutorial](tutorial.md) for a deeper dive
2. Explore [Use Cases](use_cases.md) for inspiration
3. Check out the [API Reference](api_reference.md) for more features
4. Learn about [Custom Agents](extending.md) to build your own workflows

## Common Patterns

### Using Different Models

```python
from flujo import make_agent_async

# Create a custom agent with a specific model
custom_agent = make_agent_async(
    "openai:gpt-4",  # Model identifier
    "You are a helpful AI assistant.",  # System prompt
    str  # Output type
)

# Use it in your orchestrator
flujo = Default(
    review_agent=custom_agent, 
    solution_agent=solution_agent, 
    validator_agent=validator_agent,
    reflection_agent=reflection_agent
)
```

### Structured Output

```python
from pydantic import BaseModel, Field

class CodeSnippet(BaseModel):
    language: str = Field(..., description="Programming language")
    code: str = Field(..., description="The actual code")
    explanation: str = Field(..., description="Brief explanation")

# Create an agent that outputs structured data
code_agent = make_agent_async(
    "openai:gpt-4",
    "You are a programming expert. Write clean, well-documented code.",
    CodeSnippet
)
```

### Custom Pipeline

```python
from flujo import (
    Step, Flujo, Task,
    review_agent, solution_agent, validator_agent,
)

# Define a custom pipeline (similar to the Default workflow)
custom_pipeline = (
    Step.review(review_agent)
    >> Step.solution(solution_agent)
    >> Step.validate_step(validator_agent)
)

runner = Flujo(custom_pipeline)

# The input to `run()` is the prompt for the first step.
pipeline_result = runner.run("Write a function to sort a list")

print("Pipeline steps and success states:")
for step_result in pipeline_result.step_history:
    print(f"  - {step_result.name}: {step_result.success}")

if len(pipeline_result.step_history) > 1:
    print("Solution output:\n", pipeline_result.step_history[1].output)
```

## Need Help?

- Check the [Troubleshooting Guide](troubleshooting.md)
- Join our [Discord Community](https://discord.gg/your-server)
- Open an [Issue](https://github.com/aandresalvarez/flujo/issues)
