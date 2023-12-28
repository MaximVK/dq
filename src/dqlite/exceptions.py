class DQMissingConfigFileError(Exception):
    def __init__(self, path: str) -> None:
        super().__init__(f"DQ Error: Configuration file not found at '{path}'.")
        self.path = path


class DQInvalidConfigFileError(Exception):
    def __init__(self, path: str, error_details: str) -> None:
        super().__init__(f"DQ Error: Invalid configuration file at '{path}'. Details: {error_details}")
        self.path = path


class DQUnsupportedEnvironmentType(Exception):
    def __init__(self, env_type: str) -> None:
        super().__init__(f"DQ Error: Invalid configuration file at '{env_type}'")
        self.env_type = env_type
