__version__ = "1.0.0"
__author__ = "Xplorers"
__description__ = "Di package for app"

from .domain import DependencyNotRegistered
from .container import Container

__all__ = [
    "Container",
    "DependencyNotRegistered"
]
