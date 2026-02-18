"""
Stucture:
domain: Abstacts, entites, and models ect..
application: The application of domain objects, use cases, rules, services ect...
infrastructure: Framework implementations
dependencies: Getter methods for singleton classes
interface: Access to app
"""

__version__ = "1.0.0"
__author__ = "Xplorers"
__description__ = "Crud operations for chats"


from .domain import (
    Chat,
    ChatPublic
)

from .application import (
    CreateChat
)

from .infrastructure import (
    SqlAlchemyChatsRepository
)


from .dependencies import (
    get_creat_chat_use_case,
    get_chats_repository
)
__all__ = [
    #### Domain ####
    "Chat",
    "ChatPublic",

    #### Application ####
    "CreateChat",
    

    #### Infrastructure ####
    "SqlAlchemyChatsRepository",

    #### Dependencies ####
    "get_chats_repository",
    "get_creat_chat_use_case"


]