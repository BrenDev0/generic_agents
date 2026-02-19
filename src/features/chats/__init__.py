"""
Stucture:
domain: Abstracts, entites, and models ect..
application: The application of domain objects, use cases, rules, services ect...
infrastructure: Framework implementations
dependencies: Getter methods for singleton classes
interface: Access point
"""

__version__ = "1.0.0"
__author__ = "Xplorers"
__description__ = "Chat package for app"

from .application import GetChatResource
from .dependencies import get_chat_resource_use_case

__all__ = [
    "GetChatResource",
    "get_chat_resource_use_case"
]

