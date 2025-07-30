# Python SDK for M3 Chat

[![PyPI version](https://img.shields.io/pypi/v/m3chat_sdk.svg)](https://pypi.org/project/m3chat_sdk/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Build](https://img.shields.io/github/actions/workflow/status/m3-chat/python-sdk/publish.yml?branch=main)](https://github.com/m3-chat/python-sdk/actions)

**Official Python SDK for [M3 Chat](https://m3-chat.vercel.app)** – Stream and fetch AI-generated responses from models like LLaMA, Mistral, Gemma, and more.

## Features

- Simple interface to call M3 Chat models
- Stream or fetch full responses
- Batch support (non-streaming)
- Model validation
- Typed API and clean structure
- CLI-friendly

## Installation

```bash
pip install m3chat_sdk
```

or

```bash
python3 -m pip install m3chat_sdk
```

## Quick Start

```python
from m3chat_sdk import M3ChatClient

client = M3ChatClient(stream=False)
response = client.get_response(model="mistral", content="Hello, how are you?")
print("Response:", response)
```

## Usage

### Initialize Client

```python
from m3chat_sdk import M3ChatClient

client = M3ChatClient(stream=True) # or False
```

### Get a Response

```python
response = client.get_response(model="llama3:8b", content="Explain quantum physics.")
print(response)
```

### Batch Requests (Non-Streaming)

```python
prompts = [
"What is the capital of Germany?",
"Tell me a joke.",
"What's 12 * 8?",
]

responses = client.batch_requests(messages=prompts, model="gemma")
for i, res in enumerate(responses):
print(f"Response {i + 1}: {res}")
```

## Supported Models

```python
[
"llama3:8b",
"llama2-uncensored",
"gemma3",
"gemma",
"phi3:mini",
"mistral",
"gemma:2b",
"gemma:7b",
"qwen:7b",
"qwen2.5-coder",
"qwen3",
"deepseek-coder:6.7b",
"deepseek-v2:16b",
"dolphin-mistral:7b",
"dolphin3",
"starcoder2:7b",
"magistral",
"devstral",
]
```

## Testing

Run the client test with:

```bash
python3 tests/test_client.py
```

## License

Apache License 2.0 — see [LICENSE](./LICENSE)

## Contributing

Issues and PRs welcome! [https://github.com/m3-chat/python-sdk](https://github.com/m3-chat/python-sdk)
