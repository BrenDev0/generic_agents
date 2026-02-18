class GraphQlException(Exception):
    def __init__(self, detail: str = "500"):
        self.detail = detail
        super().__init__(detail)

   