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
from pharia_inference_sdk.core.model import Llama3InstructModel
from pharia_inference_sdk.connectors import LimitedConcurrencyClient

client = LimitedConcurrencyClient()
model = Llama3InstructModel(client=client)
tracer = InMemoryTracer()

prompt = "Hello, world!"

model.generate(prompt, tracer)
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](https://github.com/Aleph-Alpha/pharia-inference-sdk/blob/main/CONTRIBUTING.md) for details on how to set up the development environment and submit changes.
