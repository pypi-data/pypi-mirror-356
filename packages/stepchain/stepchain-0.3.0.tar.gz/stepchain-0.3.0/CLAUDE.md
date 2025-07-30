# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

StepChain is a reliability layer for OpenAI's Responses API that intelligently decomposes complex tasks into chained steps. The SDK is built exclusively for the Responses API (no Chat Completions fallback) with full tool support including MCP (Model Context Protocol).

## Development Commands

### Build and Install
```bash
# Install in development mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"

# Build package
python -m build
```

### Code Quality
```bash
# Run linter
ruff check stepchain/

# Run type checker
mypy stepchain/

# Format code (ruff auto-fixes)
ruff check --fix stepchain/
```

### Running Examples
```bash
# Quick start example
python examples/quickstart.py

# Run CLI
stepchain run "Your task here" --tools web_search
```

## Architecture and Key Design Decisions

### Core Flow
1. **TaskDecomposer** breaks down complex tasks into Steps with dependencies
2. **Executor** runs the Plan using OpenAI's Responses API
3. **Storage** persists state for resume capability
4. **Retry** handles failures with exponential backoff

### Critical Constraints

1. **Responses API Only**: The SDK exclusively uses OpenAI's Responses API. Never add fallback to Chat Completions API. The `UnifiedLLMClient` enforces this by raising an error if Responses API is not available.

2. **Tool Support**: Three types of tools are supported:
   - Built-in: `web_search`, `code_interpreter` (requires container config), `file_search` (requires vector_store_ids)
   - MCP servers: Must include `type`, `server_label`, `server_url`, `allowed_tools`
   - Custom functions: Standard OpenAI function calling format

3. **Response Chaining**: Uses `previous_response_id` to maintain context across steps. The executor automatically chains responses from dependent steps.

### Key Implementation Details

- **Retry Logic**: Manual implementation without tenacity to avoid conflicts with OpenAI SDK's built-in retries
- **Tool Mapping**: `_map_tools_to_definitions()` in decomposer handles mapping LLM-suggested tools to available tool definitions
- **Storage Format**: JSONL for persistence, with each line containing a timestamped entry
- **Error Classification**: `ErrorType` enum distinguishes rate limits, server errors, tool errors for appropriate retry strategies

### Configuration

The SDK uses a zero-config approach with `setup_stepchain()`:
- Creates `.stepchain` storage directory
- Sets up logging
- Returns Config object with defaults

Environment variables:
- `OPENAI_API_KEY` (required)
- `STEPCHAIN_STORAGE_PATH` (default: `.stepchain`)
- `STEPCHAIN_LOG_LEVEL` (default: `INFO`)

### Common Patterns

When adding new features:
1. Tools must be formatted for Responses API in `executor._format_tools()`
2. All API calls go through `UnifiedLLMClient.create_completion()`
3. Steps require unique IDs matching `^[a-zA-Z0-9_-]+$`
4. Use `@retry_on_exception` decorator for retryable operations

### No Test Files

This repository intentionally contains no test files for a cleaner structure. All `test_*.py` files have been removed.