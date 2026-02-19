"""
Stucture:
domain: Abstracts, entites, and models ect..
application: The application of domain objects, use cases, rules, services ect...
infrastructure: Framework implementations
dependencies: Getter methods for singleton classes
"""
__version__ = "1.0.0"
__author__ = "Xplorers"
__description__ = "Persistance package for app"


from .domain import (
    DataRepository,
    SessionRepository,
    FileRepository,
    NotFoundException,
    UpdateFieldsException
)


from .infrastructure import (
    RedisSessionRepository,
    Boto3FileRepository,
    SqlAlchemyDataRepository,
    Base
)

from .dependencies import (
    get_session_repository
)


__all__ = [
    #### Domain ####
    "DataRepository",
    "SessionRepository",
    "FileRepository",
    "NotFoundException",
    "UpdateFieldsException",

    #### Infrastructure ####
    "RedisSessionRepository",
    "Boto3FileRepository",
    "SqlAlchemyDataRepository",
    "Base",

    #### Dependencies ####
    "get_session_repository"

]



