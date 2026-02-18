class ExpiredToken(Exception):
    def __init__(self, detail: str = "401"):
        super().__init__(detail)

class InvalidToken(Exception):
    def __init__(self, detail: str = "401"):
        super().__init__(detail)

class IncorrectPassword(Exception):
    def __init__(self, detail: str = "400"):
        super().__init__(detail)

class PermissionsException(Exception):
    def __init__(self, detail: str = "403"):
        super().__init__(detail)

class HMACException(Exception):
    def __init__(self, detail: str = "403"):
        self.detail = detail
        super().__init__(detail)