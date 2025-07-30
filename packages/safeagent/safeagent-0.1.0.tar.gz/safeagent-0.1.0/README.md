<div>
<br>
</div>

[![Version](https://img.shields.io/badge/version-0.1.0-blue)](https://pypi.org/project/minillm/)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](docs/html/index.html)

**MiniLLM** is a lightweight framework for building long-running language model workflows with durable memory and governance logging. Gemini provides the default model for generation and embeddings.

# MiniLLM

**MiniLLM** is a lightweight framework for building long‑running language model workflows with durable memory and governance logging. Gemini is the default provider for both generation and embeddings.

`minillm` is a minimal, flexible framework for orchestrating LLM workflows. It provides pluggable components for retrieval, memory, and orchestration with built in governance logging. The default configuration now targets Google's **Gemini** models for both generation and embeddings.


## Get started

Install MiniLLM:

```bash
pip install -e .[test]
```

Create a simple question-answering agent:
=======

Create a simple question-answering agent:
=======
Create a simple question‑answering agent:


```python
from minillm.pipeline import main as run_pipeline

run_pipeline()
```

Comprehensive documentation, including a Quickstart guide and API reference, is available in the [docs folder](docs/html/index.html).

## Core benefits
=======

For more information, see the [Quickstart](docs/html/quickstart.html). To learn how to build more advanced workflows or customize components, browse the [full documentation](docs/html/index.html).

## Core benefits

- Durable execution with a minimal orchestrator
- Governance logging built into every component
- Comprehensive memory with summary support
- Retrieval via FAISS or Neo4j graphs using Gemini embeddings

## MiniLLM ecosystem

MiniLLM integrates with other tools like Neo4j, Redis, and Jinja2 templates. Gemini models are configured by default through the `GEMINI_API_KEY` environment variable, but you can swap in another provider by adjusting your `Config`.

## Additional resources

- [Quickstart](docs/html/quickstart.html)
- [API Reference](docs/html/reference.html)
=======
See the [Quickstart](docs/html/quickstart.html) for details, or browse the [full HTML docs](docs/html/index.html).

## Core benefits

- **Durable execution** with a minimal orchestrator
- **Governance logging** built into every component
- **Comprehensive memory** using Redis or in‑memory storage
- **Plug‑and‑play retrieval** via FAISS or Neo4j graphs

## Ecosystem

MiniLLM integrates easily with other tools such as Neo4j, Redis, and Jinja2 templates. Gemini models provide the default LLM and embedding services, but you can swap in other providers through configuration.


## Optional Docker usage

A `Dockerfile` is included for containerized execution:

- Durable execution with a minimal orchestrator
- Governance logging built into every component
- Comprehensive memory with summary support
- Retrieval via FAISS or Neo4j graphs using Gemini embeddings
