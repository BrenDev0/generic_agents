class NotFoundException(Exception):
    def __init__(self, detail: str = "404"):
        super().__init__(detail)


class UpdateFieldsException(Exception):
    def __init__(self, detail: str ="Minimum 1 field required to perform update"):
        super().__init__(detail)