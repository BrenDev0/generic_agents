class GraphQlException(Exception):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(detail)