"""
Stucture:
domain: Abstacts, entites, and models ect..
application: The application of domain objects, use cases, rules, services ect...
infrastructure: Framework implementations
dependencies: Getter methods for singleton classes
utils: reusable functions
"""
__version__ = "1.0.0"
__author__ = "Xplorers"
__description__ = "Security package for app"


from .domain import (
    EncryptionService,
    HashingService,
    WebTokenService,
    PermissionsException,
    HMACException,
    IncorrectPassword,
    InvalidToken,
    ExpiredToken
)

from .infrastructure import (
    BcryptHashingService,
    FernetEncryptionService,
    JwtWebTokenService
)

from .dependencies import (
    get_encrytpion_service,
    get_hashing_service,
    get_web_token_service
)

from .utils import (
    get_random_code
)

__all__ = [
    #### Domain ####
    "EncryptionService",
    "HashingService",
    "WebTokenService",
    "PermissionsException",
    "HMACException",
    "InvalidToken",
    "IncorrectPassword",
    "ExpiredToken",

    #### infrastructure ####
    "BcryptHashingService",
    "FernetEncryptionService",
    "JwtWebTokenService",

    #### dependencies ####
    "get_encrytpion_service",
    "get_hashing_service",
    "get_web_token_service",

    #### utils ####
    "get_random_code"
]