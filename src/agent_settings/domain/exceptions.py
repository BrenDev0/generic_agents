class ExistingSettingsException(Exception):
    def __init__(self, detail: str = "Agent has settings"):
        super().__init__(detail)