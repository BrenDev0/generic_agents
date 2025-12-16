class PermissionsError(Exception):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(detail)