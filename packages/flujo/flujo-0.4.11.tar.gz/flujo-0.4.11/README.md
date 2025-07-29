<div align="center">
  <img src="assets/flujo.png" alt="Flujo Logo" width="180"/>
</div>

# Flujo

A powerful Python library for orchestrating AI workflows using Pydantic models.
The `flujo` package (repository hosted at
[`github.com/aandresalvarez/flujo`](https://github.com/aandresalvarez/flujo))
provides utilities to manage multi-agent pipelines with minimal setup.

## Features

- 📦 **Pydantic Native** – agents, tools, and pipeline context are all defined with Pydantic models for reliable type safety.
- 🔁 **Opinionated & Flexible** – the `Default` recipe gives you a ready‑made workflow while the DSL lets you build any pipeline.
- 🏗️ **Production Ready** – retries, telemetry, and quality controls help you ship reliable systems.
- 🧠 **Intelligent Evals** – automated scoring and self‑improvement powered by LLMs.

## Quick Start

### Installation

```bash
pip install flujo
```

### Basic Usage

```python
from flujo.recipes import Default
from flujo import (
    Task,
    review_agent, solution_agent, validator_agent,
    init_telemetry,
)

# Optional: enable telemetry for your application
init_telemetry()

# Assemble an orchestrator with the library-provided agents. The class
# runs a fixed pipeline: Review -> Solution -> Validate.
flujo = Default(
    review_agent=review_agent,
    solution_agent=solution_agent,
    validator_agent=validator_agent,
)

# Define a task
task = Task(prompt="Write a Python function to calculate Fibonacci numbers")

# Run synchronously
best_candidate = flujo.run_sync(task)

# Print the result
if best_candidate:
    print("Solution:\n", best_candidate.solution)
    if best_candidate.checklist:
        print("\nQuality Checklist:")
        for item in best_candidate.checklist.items:
            status = "✅ Passed" if item.passed else "❌ Failed"
            print(f"  - {item.description:<45} {status}")
else:
    print("No solution found.")
```

### Pipeline Example

```python
from flujo import (
    Step, Flujo, Task,
    review_agent, solution_agent, validator_agent,
)

# Build a custom pipeline using the Step DSL. This mirrors the internal
# workflow used by :class:`Default` but is fully configurable.
custom_pipeline = (
    Step.review(review_agent)
    >> Step.solution(solution_agent)
    >> Step.validate(validator_agent)
)

pipeline_runner = Flujo(custom_pipeline)

# Run synchronously; Flujo returns a PipelineResult.
pipeline_result = pipeline_runner.run(
    "Generate a REST API using FastAPI for a to-do list application."
)

print("\nPipeline Execution History:")
for step_res in pipeline_result.step_history:
    print(f"- Step '{step_res.name}': Success={step_res.success}")

if len(pipeline_result.step_history) > 1 and pipeline_result.step_history[1].success:
    solution_output = pipeline_result.step_history[1].output
    print("\nGenerated Solution:\n", solution_output)
```

## Documentation

### Getting Started

- [Installation Guide](docs/installation.md): Detailed installation instructions
- [Quickstart Guide](docs/quickstart.md): Get up and running quickly
- [Core Concepts](docs/concepts.md): Understand the fundamental concepts

### User Guides

- [Usage Guide](docs/usage.md): Learn how to use the library effectively
- [Configuration Guide](docs/configuration.md): Configure the orchestrator
- [Tools Guide](docs/tools.md): Create and use tools with agents
- [Pipeline DSL Guide](docs/pipeline_dsl.md): Build custom workflows
- [Scoring Guide](docs/scoring.md): Implement quality control
- [Telemetry Guide](docs/telemetry.md): Monitor and analyze usage

### Advanced Topics

- [Extending Guide](docs/extending.md): Create custom components
- [Use Cases](docs/use_cases.md): Real-world examples and patterns
- [API Reference](docs/api_reference.md): Detailed API documentation
- [Troubleshooting Guide](docs/troubleshooting.md): Common issues and solutions

### Development

- [Contributing Guide](CONTRIBUTING.md): How to contribute to the project
- [Development Guide](docs/dev.md): Development setup and workflow
- [Code of Conduct](CODE_OF_CONDUCT.md): Community guidelines
- [License](LICENSE): Dual License (AGPL-3.0 + Commercial)

## Examples

Check out the [examples directory](examples/) for more usage examples:

| Script | What it shows |
| ------ | ------------- |
| [**00_quickstart.py**](examples/00_quickstart.py) | Hello World with the Default recipe. |
| [**01_weighted_scoring.py**](examples/01_weighted_scoring.py) | Weighted scoring to prioritize docstrings. |
| [**02_custom_agents.py**](examples/02_custom_agents.py) | Building creative agents with custom prompts. |
| [**03_reward_scorer.py**](examples/03_reward_scorer.py) | Using an LLM judge via RewardScorer. |
| [**04_batch_processing.py**](examples/04_batch_processing.py) | Running multiple workflows concurrently. |
| [**05_pipeline_sql.py**](examples/05_pipeline_sql.py) | Pipeline DSL with SQL validation plugin. |
| [**06_typed_context.py**](examples/06_typed_context.py) | Sharing state with Typed Pipeline Context. |
| [**07_loop_step.py**](examples/07_loop_step.py) | Iterative refinement using LoopStep. |
| [**08_branch_step.py**](examples/08_branch_step.py) | Dynamic routing with ConditionalStep. |

Looking for more community resources? Check out the [Awesome Flujo list](AWESOME-FLUJO.md).

## Requirements

- Python 3.11 or higher
- OpenAI API key (for OpenAI models)
- Anthropic API key (for Claude models)
- Google API key (for Gemini models)

## Installation

### Basic Installation

```bash
pip install flujo
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/aandresalvarez/flujo.git
cd flujo

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## Support

- [Documentation](https://flujo.readthedocs.io/)
- [Issue Tracker](https://github.com/aandresalvarez/flujo/issues)
- [Discussions](https://github.com/aandresalvarez/flujo/discussions)
- [Discord](https://discord.gg/...)

## License

This project is dual-licensed:

1. **Open Source License**: GNU Affero General Public License v3.0 (AGPL-3.0)
   - Free for open-source projects
   - Requires sharing of modifications
   - Suitable for non-commercial use

2. **Commercial License**
   - For businesses and commercial use
   - Includes support and updates
   - No requirement to share modifications
   - Contact for pricing and terms

For commercial licensing, please contact: alvaro@example.com

See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE](COMMERCIAL_LICENSE) for details.

## Acknowledgments

- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
- [OpenAI](https://openai.com/) for GPT models
- [Anthropic](https://www.anthropic.com/) for Claude models
- [Google](https://ai.google.dev/) for Gemini models
- All our contributors and users

## Citation

If you use this project in your research, please cite:

```bibtex
@software{flujo,
  author = {Alvaro Andres Alvarez},
  title = {Flujo},
  year = {2024},
  url = {https://github.com/aandresalvarez/flujo}
}
```
