"""
Stucture:
domain: Abstacts, entites, and models ect..
interface: access point
setup: basic setup
"""
__version__ = "1.0.0"
__author__ = "Xplorers"
__description__ = "Api package for app"


from .domain import GraphQlException
from .interface import validate_input_to_model, inject_strawberry_context

__all__ = [
    #### Domain ####
    "GraphQlException",

    #### Interface ####
    "validate_input_to_model",
    "inject_strawberry_context"
]
