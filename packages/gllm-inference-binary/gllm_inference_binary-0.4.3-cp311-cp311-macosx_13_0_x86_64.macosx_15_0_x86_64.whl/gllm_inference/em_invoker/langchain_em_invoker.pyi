from _typeshed import Incomplete
from gllm_inference.em_invoker.em_invoker import BaseEMInvoker as BaseEMInvoker
from gllm_inference.schema import Vector as Vector
from langchain_core.embeddings import Embeddings as Embeddings

class LangChainEMInvoker(BaseEMInvoker):
    """An embedding model invoker to interact with embedding models defined using LangChain's Embeddings.

    The `LangChainEMInvoker` class is responsible for invoking an embedding model defined using LangChain's
    Embeddings module. It uses the embedding model to transform the input text or list of texts into their
    vector representations.

    Attributes:
        em (Embeddings): The instance to interact with an embedding model defined using LangChain's Embeddings.
    """
    em: Incomplete
    def __init__(self, em: Embeddings) -> None:
        """Initializes a new instance of the LangChainEMInvoker class.

        Args:
            em (Embeddings): The instance to interact with an embedding model defined using LangChain's Embeddings.
        """
    def to_langchain(self) -> Embeddings:
        """Converts the current embedding model invoker to an instance of LangChain `Embeddings` object.

        Returns:
            Embeddings: An instance of LangChain `Embeddings` object.
        """
