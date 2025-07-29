<div align="center">
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="./assets/paid_light.svg" width=600>
        <source media="(prefers-color-scheme: light)" srcset="./assets/paid_dark.svg" width=600>
        <img alt="Fallback image description" src="./assets/paid_light.svg" width=600>
    </picture>
</div>

# 

<div align="center">
    <a href="https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2FAgentPaid%2Fpaid-python">
        <img src="https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen" alt="fern shield">
    </a>
    <a href="https://pypi.org/project/paid-python">
        <img src="https://img.shields.io/pypi/v/paid-python" alt="pypi shield">
    </a>
</div>

Paid is the all-in-one, drop-in Business Engine for AI Agents that handles your pricing, subscriptions, margins, billing, and renewals with just 5 lines of code. 
The Paid Python library provides convenient access to the Paid API from Python applications.

## Documentation

See the full API docs [here](https://paid.docs.buildwithfern.com/api-reference/api-reference/customers/list)

## Installation

You can install the package using pip:

```bash
pip install paid-python
```

## Usage

The client needs to be configured with your account's API key, which is available in the [Paid dashboard](https://app.paid.ai/agent-integration/api-keys). 

```python
from paid import Client

client = Paid(token="API_KEY")

client.customers.create(
    name="name"
)
```

## Request And Response Types

The SDK provides Python classes for all request and response types. These are automatically handled when making API calls.

```python
# Example of creating a customer
response = client.customers.create(
    name="John Doe",
)

# Access response data
print(response.name)
print(response.email)
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), the SDK will raise an appropriate error.

```python
try:
    client.customers.create(...)
except paid.Error as e:
    print(e.status_code)
    print(e.message)
    print(e.body)
    print(e.raw_response)
```

## Logging

Supported log levels are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.

For example, to set the log level to debug, you can set the environment variable:
```bash
export PAID_LOG_LEVEL=DEBUG
```
Falls back to `INFO`

## Cost Tracking

As of now, the following OpenAI python APIs are supported:

```
chat.completions.create()
responses.create()
images.generate()
embeddings.create()
```

Example usage:

```python
import os
from openai import OpenAI
import dotenv
from paid import Paid
from paid.tracing.wrappers import PaidOpenAI

# Initialize Paid SDK
client = Paid(token="PAID_API_KEY")

# Initialize OpenAI client
_ = dotenv.load_dotenv()

openAIClient = PaidOpenAI(OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_KEY"),
))

# Initialize tracing, must be after initializeing Paid SKD
client.initialize_tracing()

# Capture chat request in telemetry
def chat_complete1():
    response = openAIClient.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a coding assistant that talks like a pirate."},
            {"role": "user", "content": "How do I check if a Python object is an instance of a class?"}
        ]
    )
    return response

def chat_complete2():
    response = openAIClient.responses.create(
        model="gpt-4o",
        instructions="You are a historian.",
        input="When did Boston tea party happen?",
    )
    return response

def embeddings():
    response = openAIClient.embeddings.create(
        model="text-embedding-3-small",
        input=["Hello world", "How are you?"]
    )
    return response

def image_generate():
    response = openAIClient.images.generate(
        model="dall-e-3",
        prompt="A sunset over mountains",
        size="1024x1024",
        quality="hd",
        style="vivid",
        n=1
    )
    return response

def do_agent_work():
    chat_complete1()
    chat_complete2()
    image_generate()
    embeddings()

# Finally, Capture the traces!
_ = client.capture("your_external_customer_id", do_agent_work)
```


## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
