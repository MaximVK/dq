from dataclasses import dataclass, field
from typing import Optional, Dict
from pydantic import BaseModel, ValidationError, SecretStr
import yaml
from dq.exceptions import DQMissingConfigFileError, DQInvalidConfigFileError

class EnvironmentCredentials(BaseModel):
    user: str
    password: SecretStr

class SecretsFile(BaseModel):
    databases: Dict[str, EnvironmentCredentials]

class Environment(BaseModel):
    name: str
    conn: str
    path: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[SecretStr] = None
    database: Optional[str] = None

class TestResultLogger(BaseModel):
    name: str
    target: str
    folder_path: Optional[str] = None
    db_env: Optional[str] = None

class Configuration(BaseModel):
    environments: Dict[str, Environment]

    def get_environment_by_name(self, name: str) -> Optional[Environment]:
        return self.environments.get(name, None)


def load_secrets(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            secrets_data = yaml.safe_load(file)
            validated_secrets = SecretsFile(databases=secrets_data)
    except FileNotFoundError:
        raise DQMissingConfigFileError(file_path)
    except (yaml.YAMLError, ValidationError) as e:
        raise DQInvalidConfigFileError(file_path, str(e))
    
    return validated_secrets


def load_config(config_path: str, secrets_path: Optional[str] = None) -> Configuration:
    try:
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)
            environments = {name: Environment(name=name, **data) for name, data in config_data['Environments'].items()}

        if secrets_path:
            secrets = load_secrets(secrets_path)
            for name, env in environments.items():
                env_secrets = secrets[name]
                env.user = env_secrets.user
                env.password = env_secrets.password
            validated_config = Configuration(environments=environments)
    except FileNotFoundError:
        raise DQMissingConfigFileError(config_path)
    except (yaml.YAMLError, ValidationError) as e:
        raise DQInvalidConfigFileError(config_path, str(e))
    
    return validated_config 