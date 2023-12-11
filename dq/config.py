from dataclasses import dataclass, field
from typing import Optional, Dict
import yaml

@dataclass
class Environment:
    name: str
    conn: str
    path: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = field(default=None, repr=False)
    database: Optional[str] = None

    def load_password(self, secrets: dict):
        if self.name in secrets:
            env_secrets = secrets[self.name]
            self.user = env_secrets.get('user')
            self.password = env_secrets.get('password')
    
@dataclass
class TestResultLogger:
    name: str
    target: str
    folder_path: Optional[str] = None
    db_env: Optional[str] = None


@dataclass
class Configuration:
    environments: Dict[str, Environment]
    loggers: Dict[str, Logger]

    def get_environment_by_name(self, name: str) -> Optional[Environment]:
        return self.environments.get(name, None)


def load_secrets(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")
    except Exception as e:
        raise ValueError(f"Error loading secrets file: {e}")


def load_config(config_path: str, secrets_path: Optional[str] = None) -> Configuration:
    try:
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)
            environments = {name: Environment(name, **data) for name, data in config_data['Environments'].items()}
            loggers = {name: TestResultLogger(name, **data) for name, data in config_data['Loggers'].items()}
            if secrets_path:
                secrets = load_secrets(secrets_path)
                for name, env in environments.items():
                    env.load_password(secrets)
            return Configuration(environments=environments, loggers=loggers)
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")
    except Exception as e:
        raise ValueError(f"Error loading config file: {e}")