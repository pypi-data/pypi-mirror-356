import abc
from _typeshed import Incomplete
from abc import ABC
from gllm_inference.constants import ALL_EXTENSIONS as ALL_EXTENSIONS, DOCUMENT_MIME_TYPES as DOCUMENT_MIME_TYPES
from gllm_inference.schema import Attachment as Attachment, AttachmentType as AttachmentType, EMContent as EMContent, Vector as Vector
from langchain_core.embeddings import Embeddings as Embeddings
from typing import Any

class BaseEMInvoker(ABC, metaclass=abc.ABCMeta):
    """A base class for embedding model invokers used in Gen AI applications.

    The `BaseEMInvoker` class provides a framework for invoking embedding models.

    Attributes:
        default_hyperparameters (dict[str, Any]): Default hyperparameters for invoking the embedding model.
    """
    default_hyperparameters: Incomplete
    def __init__(self, default_hyperparameters: dict[str, Any] | None = None, valid_extensions_map: dict[str, set[str]] | None = None, langchain_kwargs: dict[str, Any] | None = None) -> None:
        '''Initializes a new instance of the BaseEMInvoker class.

        Args:
            default_hyperparameters (dict[str, Any] | None, optional): Default hyperparameters for invoking the
                embedding model. Defaults to None, in which case an empty dictionary is used.
            valid_extensions_map (dict[str, set[str]] | None, optional): A dictionary mapping for validating the
                content type of the multimodal inputs. They keys are the mime types (e.g. "image") and the values are
                the set of valid file extensions for the corresponding mime type. Defaults to None, in which case an
                empty dictionary is used.
            langchain_kwargs (dict[str, Any] | None, optional): Additional keyword arguments to initiate the LangChain
                embedding model. Defaults to None.
        '''
    async def invoke(self, content: EMContent | list[EMContent], hyperparameters: dict[str, Any] | None = None) -> Vector | list[Vector]:
        """Invokes the embedding model with the provided content or list of contents.

        Args:
            content (EMContent | list[EMContent]): The input or list of inputs to be embedded using the embedding model.
            hyperparameters (dict[str, Any] | None, optional): A dictionary of hyperparameters for the embedding model.
                Defaults to None, in which case the default hyperparameters are used.

        Returns:
            Vector | list[Vector]: The vector representations of the input contents:
                1. If the input is an `EMContent`, the output is a `Vector`.
                2. If the input is a `list[EMContent]`, the output is a `list[Vector]`.

        Raises:
            ValueError: If the input content is invalid.
        """
    def to_langchain(self) -> Embeddings:
        """Converts the current embedding model invoker to an instance of LangChain `Embeddings` object.

        This method converts the EM invoker to an instance of LangChain's `Embeddings` object.
        This method requires the appropriate `langchain-<provider>` package to be installed.

        Returns:
            Embeddings: An instance of LangChain `Embeddings` object.

        Raises:
            ValueError: If `langchain_module_name` or `langchain_class_name` is missing.
        """
