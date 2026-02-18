"""
Stucture:
domain: Abstacts, entites, and models ect..
application: The application of domain objects, use cases, rules, services ect...
infrastructure: Framework implementations
interface: access point
dependencies: Getter methods for singleton classes
"""
__version__ = "1.0.0"
__author__ = "Xplorers"
__description__ = "knowledge package for app"

from  .dependencies import (
    get_update_embeddings_tracker_use_case
)

__all__ = [
    ### Dependencies ###
]