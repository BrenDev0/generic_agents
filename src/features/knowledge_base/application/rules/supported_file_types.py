from ...domain import UnsupportedFileType

class IsSupportedFileType:
    def validate(
        self,
        file_type: str
    ):
        supported = [
            "application/pdf",           # .pdf
            "text/plain",                # .txt
            "text/markdown",             # .md
        ]

        if file_type not in supported:
            raise UnsupportedFileType(f"Unsupported file type: {file_type}. Supported types: {', '.join(supported)}")
        
        return True