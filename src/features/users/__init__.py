"""
Stucture:
domain: Abstracts, entites, and models ect..
application: The application of domain objects, use cases, rules, services ect...
infrastructure: Framework implementation of domain abstracts
interface: access point
dependencies: Getter methods for singleton classes
"""
__version__ = "1.0.0"
__author__ = "Xplorers"
__description__ = "Users package for app"

from .domain import (
    EmailInUseException
)

from .dependencies import (
    get_users_repository,
    get_unique_email_rule, 
    get_user_exists_rule
)

__all__ = [
    #### Domain ####
    "EmailInUseException",

    #### Dependencies ####
    "get_users_repository",
    "get_unique_email_rule", 
    "get_user_exists_rule",
]
