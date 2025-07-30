from gllm_inference.em_invoker.langchain_em_invoker import LangChainEMInvoker as LangChainEMInvoker
from gllm_inference.utils.retry import RetryConfig as RetryConfig
from typing import Any

class OpenAIEMInvoker(LangChainEMInvoker):
    """An embedding model invoker to interact with embedding models hosted through OpenAI API endpoints.

    The `OpenAIEMInvoker` class is responsible for invoking an embedding model using the OpenAI API.
    It uses the embedding model to transform a text or a list of input text into their vector representations.

    Attributes:
        em (OpenAIEmbeddings): The embedding model instance to interact with OpenAI models.
        retry_config (RetryConfig): The retry configuration for the embedding model.
    """
    def __init__(self, model_name: str, api_key: str, model_kwargs: Any = None, retry_config: RetryConfig | None = None) -> None:
        """Initializes a new instance of the OpenAIEMInvoker class.

        Args:
            model_name (str): The name of the OpenAI model to be used.
            api_key (str): The API key for accessing the OpenAI model.
            model_kwargs (Any, optional): Additional keyword arguments to initiate the OpenAI model. Defaults to None.
            retry_config (RetryConfig | None, optional): The retry configuration for the embedding model.
                Defaults to None, in which case a default config with no retry and 30.0 seconds timeout is used.
        """
