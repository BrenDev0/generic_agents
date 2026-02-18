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

__all__ = [
    "GraphQlException"
]
