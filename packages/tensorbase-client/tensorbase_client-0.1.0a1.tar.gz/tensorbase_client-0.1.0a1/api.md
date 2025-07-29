# Tensorbase

Types:

```python
from tensorbase_client.types import HealthCheckResponse
```

Methods:

- <code title="get /">client.<a href="./src/tensorbase_client/_client.py">health_check</a>() -> <a href="./src/tensorbase_client/types/health_check_response.py">HealthCheckResponse</a></code>

# Chat

Types:

```python
from tensorbase_client.types import ChatGenerateCompletionResponse
```

Methods:

- <code title="post /chat/completions">client.chat.<a href="./src/tensorbase_client/resources/chat.py">generate_completion</a>(\*\*<a href="src/tensorbase_client/types/chat_generate_completion_params.py">params</a>) -> <a href="./src/tensorbase_client/types/chat_generate_completion_response.py">ChatGenerateCompletionResponse</a></code>

# Images

Types:

```python
from tensorbase_client.types import ImageGenerateResponse
```

Methods:

- <code title="post /v1/images/generations">client.images.<a href="./src/tensorbase_client/resources/images.py">generate</a>(\*\*<a href="src/tensorbase_client/types/image_generate_params.py">params</a>) -> <a href="./src/tensorbase_client/types/image_generate_response.py">ImageGenerateResponse</a></code>

# Models

Types:

```python
from tensorbase_client.types import ModelRetrieveResponse, ModelListResponse
```

Methods:

- <code title="get /models/{model}">client.models.<a href="./src/tensorbase_client/resources/models.py">retrieve</a>(model) -> <a href="./src/tensorbase_client/types/model_retrieve_response.py">ModelRetrieveResponse</a></code>
- <code title="get /models">client.models.<a href="./src/tensorbase_client/resources/models.py">list</a>() -> <a href="./src/tensorbase_client/types/model_list_response.py">ModelListResponse</a></code>
