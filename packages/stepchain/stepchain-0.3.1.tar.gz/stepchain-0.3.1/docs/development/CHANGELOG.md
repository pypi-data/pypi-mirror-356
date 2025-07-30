# Changelog

All notable changes to StepChain will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2025-06-21

### 🐛 Bug Fixes
- Fixed critical issue with tool mapping in decomposer where tool descriptions were not properly passed
- Fixed tool name vs description confusion in plan generation
- Consolidated TaskDecomposer implementations to eliminate code duplication

### 📚 Documentation
- Added performance comparison documentation
- Improved PyPI compatibility and package metadata
- Updated examples and README clarity

### 🔧 Internal
- Refactored decomposer module to use single implementation
- Improved error handling in tool execution
- Enhanced type safety in tool configurations

## [0.3.0] - 2025-06-20

### 🚀 Initial Release

**StepChain** - The thinnest possible layer for reliable AI workflows. 185 lines of core code that make OpenAI's Responses API actually useful.

### ✨ Features

#### Core API
- **Simple 2-function API**: Just `decompose()` and `execute()`
- **Intelligent task decomposition**: Automatically breaks complex tasks into executable steps with dependencies
- **State persistence**: JSONL-based storage with automatic resume capability
- **Smart retry logic**: Single retry takes success rate from 90% to 99%
- **Parallel execution**: DAG scheduler automatically parallelizes independent steps

#### Tool Support
- **Built-in tools**: 
  - `web_search` - Search the web
  - `code_interpreter` - Execute Python code (requires container config)
  - `file_search` - Search vector stores (requires vector_store_ids)
- **MCP (Model Context Protocol)**: Full support for OpenAI's MCP specification
  - Connect to any external service
  - Approval modes: "always" or "never"
  - Multi-server support in single plan
- **Custom functions**: Register Python functions as tools with automatic schema generation

#### CLI Commands
- `stepchain run` - Execute tasks or plans
- `stepchain resume` - Resume interrupted runs  
- `stepchain validate` - Validate plan YAML files
- `stepchain decompose` - Decompose tasks into plans
- `stepchain list-runs` - List all execution runs

#### Architecture
- **OpenAI Responses API exclusive**: No fallback to Chat Completions (by design)
- **Zero configuration**: Single `setup_stepchain()` call
- **Pluggable storage**: Abstract interface, JSONL implementation included
- **Function registry**: Safe execution with timeout protection
- **Compression strategies**: Configurable history compression
- **Type-safe**: Full type hints with Pydantic models

#### Developer Experience
- **Python 3.12+**: Modern Python with latest features
- **Rich terminal output**: Beautiful progress bars and formatted results
- **Async support**: Both sync and async executors
- **Validation**: Automatic plan and step validation
- **Error classification**: Distinguishes rate limits, server errors, tool errors

### 📚 Documentation
- Comprehensive README with philosophy and examples
- API reference for all modules
- MCP integration examples from OpenAI cookbook
- Architecture documentation
- Development guide

### 🎯 Philosophy
1. **Trust the LLM** - It's smarter than your validation code
2. **Fail fast** - Bad outputs are upstream bugs  
3. **Delete code** - Every line is a potential bug

### 📦 Dependencies
- `openai>=1.0` - OpenAI Python SDK
- `pydantic>=2.0` - Data validation
- `rich>=13.0` - Terminal formatting
- `click>=8.0` - CLI framework
- `pyyaml>=6.0` - YAML support
- `opentelemetry-sdk>=1.20` - Observability

### 🚧 Known Limitations
- Requires OpenAI Responses API access (beta)
- No streaming support (intentional - adds complexity)
- No built-in cost tracking (use OpenAI dashboard)
- Single retry only (more would mask real issues)

---

*"Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away." - Antoine de Saint-Exupéry*