class GraphQlException(Exception):
    def __init__(self, detail: str = "Bad Request", code: str = ""):
        self.detail = detail
        self.code = code
        super().__init__(detail)

    def to_dict(self):
        return {
            "message": self.detail,
            "extensions": {
                "code": self.code
            }
        }