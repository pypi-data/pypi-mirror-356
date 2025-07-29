from abc import ABC, abstractmethod

class FormatterBase(ABC):
    """
    Abstract base class for formatters.
    """
    @abstractmethod
    def format(self, text: str) -> str:
        pass
