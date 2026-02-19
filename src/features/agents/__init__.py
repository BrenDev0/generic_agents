"""
Stucture:
domain: Abstracts, entites, and models ect..
application: The application of domain objects, use cases, rules, services ect...
infrastructure: Framework implementations
interface: access point
dependencies: Getter methods for singleton classes
"""
__version__ = "1.0.0"
__author__ = "Xplorers"
__description__ = "agent package for app"

from .domain import (
    Agent,
    AgentPublic
)

from .infrastructure import SqlAlchemyAgent
from .dependencies import get_agents_repository

__all__ = [
    #### Domain ####
    "Agent",
    "AgentPublic",

    #### Infrastructure ####
    "SqlAlchemyAgent",

    #### Dependencies ####
    "get_agents_repository"
]
