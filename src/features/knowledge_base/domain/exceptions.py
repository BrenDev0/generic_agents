class UnsupportedFileType(Exception):
    def __init__(self, detail: str = "Unsupported file type"):
        super().__init__(detail)