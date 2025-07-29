<!--
SPDX-FileCopyrightText: 2024 CSC - IT Center for Science Oy

SPDX-License-Identifier: MIT
-->

# Python client for Aitta HPC ML inference platform

A Python client library for the Aitta ML inference platform for HPC systems.

Note that both the API as well as the client libary are still under heavy development and while
we try to keep changes mostly backwards-compatible, breaking changes may happen. Access to Aitta is
currently restricted to selected beta users.

## Main client API classes

- `Client`: implements all requests to the Aitta API servers on a low level and is used by all other classes
- `AccessTokenSource`: used by the client to get (and eventually refresh) access tokens
- `Model`: represents a model and provides methods to perform inference
- `Task`: represents an active inference task and provides methods to query the current status and results

## Example usage

The below shows two examples for usage of the Aitta API using the Python client library.

For accessing the Aitta API the client will need a way to obtain access tokens, which is
implemented in the form of an `AccessTokenSource`. For the time being, you can generate a static
model-specific token at the [web frontend](https://staging-aitta.2.rahtiapp.fi/) by opening
the model's page, switching to the "API Key" tab and pressing the "Generate API key" button.

With the token thus obtained, then have to create an instance of `StaticAccessTokenSource` for use
with the client library.

### Performing text completion with the LumiOpen/Poro model
```python
from aitta_client import Model, Client, StaticAccessTokenSource

# configure Client instance with access token and API URL
poro_access_token = "<generate your model-specific token from https://staging-aitta.2.rahtiapp.fi/ and enter it here>"

token_source = StaticAccessTokenSource(poro_access_token)
client = Client("https://api-staging-aitta.2.rahtiapp.fi", token_source)

# load the LumiOpen/Poro model
model = Model.load("LumiOpen/Poro", client)

print(model.description)

# declare inputs and parameters for a text completion inference task
inputs = {
    'input': 'Suomen paras kaupunki on'
}

params = {
    'do_sample': True,
    'max_new_tokens': 20
}

print(f"INPUT:\n{inputs}")

# start the inference and wait for completion
result = model.start_and_await_inference(inputs, params)
print(f"OUTPUT:\n{result}")

```

### Performing OpenAI chat completion with the LumiOpen/Poro-34b-chat model

```python
from aitta_client import Model, Client, StaticAccessTokenSource
import openai

# configure Client instance with access token and API URL
poro_access_token = "<generate your model-specific token from https://staging-aitta.2.rahtiapp.fi/ and enter it here>"

token_source = StaticAccessTokenSource(poro_access_token)
client = Client("https://api-staging-aitta.2.rahtiapp.fi", token_source)

# load the LumiOpen/Poro-34B-chat model
model = Model.load("LumiOpen/Poro-34B-chat", client)

print(model.description)

# configure OpenAI client to use the Aitta OpenAI compatibility endpoints
client = openai.OpenAI(api_key=token_source.get_access_token(), base_url=model.openai_api_url)

# perform chat completion with the OpenAI client
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test"
        }
    ],
    model=model.id,
    stream=False  # response streaming is currently not supported by Aitta
)

print(chat_completion.choices[0].message.content)
```
