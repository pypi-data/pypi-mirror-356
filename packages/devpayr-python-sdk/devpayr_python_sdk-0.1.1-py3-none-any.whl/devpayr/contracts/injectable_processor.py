from abc import ABC, abstractmethod
from typing import Dict


class InjectableProcessorInterface(ABC):
    """
    Interface for custom injectable processors.
    Must implement a static `handle()` method.
    """

    @staticmethod
    @abstractmethod
    def handle(
        injectable: Dict,
        secret: str,
        base_path: str,
        verify_signature: bool = True
    ) -> str:
        """
        Handle a single injectable.
        Should decrypt, verify, and store/process as needed.
        """
        pass
