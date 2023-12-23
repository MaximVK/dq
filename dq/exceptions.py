
class DQMissingConfigFileError(Exception):
    def __init__(self, path: str) -> None:
        super().__init__(f"DQ Error: Configuration file not found at '{path}'.")
        self.path = path


class DQInvalidConfigFileError(Exception):
    def __init__(self, path: str, error_details: str) -> None:
        super().__init__(f"DQ Error: Invalid configuration file at '{path}'. Details: {error_details}")
        self.path = path
