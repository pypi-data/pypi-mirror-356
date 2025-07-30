from _typeshed import Incomplete
from gllm_inference.em_invoker.em_invoker import BaseEMInvoker as BaseEMInvoker
from gllm_inference.em_invoker.schema.voyage import InputType as InputType, Key as Key
from gllm_inference.schema import Attachment as Attachment, AttachmentType as AttachmentType, EMContent as EMContent, Vector as Vector
from typing import Any

VALID_EXTENSIONS_MAP: Incomplete
MAX_PYTHON_MINOR_VERSION: int

class VoyageEMInvoker(BaseEMInvoker):
    '''An embedding model invoker to interact with Voyage embedding models.

    Attributes:
        client (Client): The client for the Voyage API.
        model_name (str): The name of the Voyage embedding model to be used.
        default_hyperparameters (dict[str, Any]): Default hyperparameters for invoking the embedding model.

    Input types:
        The `VoyageEMInvoker` supports the following input types:
        1. Text.
        2. Image: ".png", ".jpeg", and ".jpg".
        3. A tuple containing text and image.
        Non-text inputs must be passed as a `Attachment` object.

    Output format:
        The `VoyageEMInvoker` can embed either:
        1. A single content.
           1. A single content is either a text, an image, or a tuple containing a text and an image.
           2. The output will be a `Vector`, representing the embedding of the content.

           # Example 1: Embedding a text content.
           ```python
           text = "What animal is in this image?"
           result = await em_invoker.invoke(text)
           ```

           # Example 2: Embedding an image content.
           ```python
           image = Attachment.from_path("path/to/local/image.png")
           result = await em_invoker.invoke(image)
           ```

           # Example 3: Embedding a tuple containing a text and an image.
           ```python
           text = "What animal is in this image?"
           image = Attachment.from_path("path/to/local/image.png")
           result = await em_invoker.invoke((text, image))
           ```

           The above examples will return a `Vector` with a size of (embedding_size,).

        2. A list of contents.
           1. A list of contents is a list that consists of any of the above single contents.
           2. The output will be a `list[Vector]`, where each element is a `Vector` representing the
              embedding of each single content.

           # Example: Embedding a list of contents.
           ```python
           text = "What animal is in this image?"
           image = Attachment.from_path("path/to/local/image.png")
           mix_content = (text, image)
           result = await em_invoker.invoke([text, image, mix_content])
           ```

           The above examples will return a `list[Vector]` with a size of (3, embedding_size).
    '''
    client: Incomplete
    model_name: Incomplete
    def __init__(self, model_name: str, api_key: str | None = None, model_kwargs: dict[str, Any] | None = None, default_hyperparameters: dict[str, Any] | None = None) -> None:
        """Initializes a new instance of the VoyageEMInvoker class.

        Args:
            model_name (str): The name of the Voyage embedding model to be used.
            api_key (str | None, optional): The API key for the Voyage API. Defaults to None, in which
                case the `VOYAGE_API_KEY` environment variable will be used.
            model_kwargs (dict[str, Any] | None, optional): Additional keyword arguments for the Voyage client.
                Defaults to None.
            default_hyperparameters (dict[str, Any] | None, optional): Default hyperparameters for invoking the model.
                Defaults to None.
        """
