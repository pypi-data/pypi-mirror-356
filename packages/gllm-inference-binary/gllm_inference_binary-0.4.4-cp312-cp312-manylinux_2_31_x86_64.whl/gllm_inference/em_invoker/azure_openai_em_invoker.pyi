from gllm_inference.em_invoker.langchain_em_invoker import LangChainEMInvoker as LangChainEMInvoker
from gllm_inference.utils.retry import RetryConfig as RetryConfig
from typing import Any

class AzureOpenAIEMInvoker(LangChainEMInvoker):
    """An embedding model invoker to interact with embedding models hosted through Azure OpenAI API endpoints.

    The `AzureOpenAIEMInvoker` class is responsible for invoking an embedding model using the Azure OpenAI API.
    It uses the embedding model to transform a text or a list of input text into their vector representations.

    Attributes:
        em (AzureOpenAIEmbeddings): The embedding model instance to interact with Azure OpenAI models.
        retry_config (RetryConfig): The retry configuration for the embedding model.
    """
    def __init__(self, model_name: str, api_key: str, azure_deployment: str, azure_endpoint: str, api_version: str, model_kwargs: dict[str, Any] = None, retry_config: RetryConfig | None = None) -> None:
        """Initializes a new instance of the AzureOpenAIEMInvoker class.

        Args:
            model_name (str): The name of the Azure OpenAI model to be used.
            api_key (str): The API key for accessing the Azure OpenAI model.
            azure_deployment (str): The name of the Azure OpenAI deployment to use.
            azure_endpoint (str): The URL endpoint for the Azure OpenAI service.
            api_version (str): The API version of the Azure OpenAI service.
            model_kwargs (dict[str, Any], optional): Additional keyword arguments to initiate the Azure OpenAI model.
                Defaults to None.
            retry_config (RetryConfig | None, optional): The retry configuration for the embedding model.
                Defaults to None, in which case a default config with no retry and 30.0 seconds timeout is used.
        """
