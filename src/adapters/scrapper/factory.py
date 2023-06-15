from typing import Optional, Type
from .interface import ScrapperInterface
from .bs4.adapter import BS4ScrapperAdapter


def get_adapter(client_name: Optional[str] = "BS4") -> Type[ScrapperInterface]:
    if client_name == "BS4":
        return BS4ScrapperAdapter
