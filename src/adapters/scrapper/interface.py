from typing import Optional
from abc import ABC, abstractmethod


class ScrapperInterface(ABC):

    @abstractmethod
    def get_html(self):
        raise NotImplementedError

    @abstractmethod
    def get_text_by_span_id(self, span_id: str) -> Optional[str]:
        raise NotImplementedError
