# pharia-inference-sdk

Formerly the `intelligence_layer/core` package.

## Overview

The pharia-inference-sdk provides essential functionality for the intelligence layer.

## Installation
The SDK is published on [PyPI](https://pypi.org/project/pharia-inference-sdk/).

To add the SDK as a dependency to an existing project managed, run
```bash
pip install pharia-inference-sdk
```

## Usage

```python
from pharia_inference_sdk.core.tracer import InMemoryTracer
from pharia_inference_sdk.core.model import Llama3InstructModel, Prompt, CompleteInput
from aleph_alpha_client import Client

client=Client(token="<token>", host="<inference-api-url>")
model = Llama3InstructModel(client=client)
tracer = InMemoryTracer()

prompt = Prompt.from_text(text="What is the most common fish in swedish lakes?")
model.complete(CompleteInput(prompt=prompt, maximum_tokens=32), tracer)

# see trace in rich format
tracer._rich_render_()
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](https://github.com/Aleph-Alpha/pharia-inference-sdk/blob/main/CONTRIBUTING.md) for details on how to set up the development environment and submit changes.
