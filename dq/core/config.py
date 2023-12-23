from typing import Optional, Dict
from pydantic import BaseModel, ValidationError, SecretStr
import yaml
from dq.exceptions import DQMissingConfigFileError, DQInvalidConfigFileError


class GlobalSettings(BaseModel):
    default_output_env: str


class EnvironmentCredentials(BaseModel):
    user: str
    password: SecretStr


class SecretsFile(BaseModel):
    environments: Dict[str, EnvironmentCredentials]


class Environment(BaseModel):
    name: str
    env_type: str
    is_output: Optional[bool] = False


class FileSystemEnvironment(Environment):
    path: str
    user: Optional[str] = None
    password: Optional[SecretStr] = None
    output_folder: Optional[str] = None


class DatabaseEnvironment(Environment):
    path: Optional[str] = None
    database: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[SecretStr] = None
    output_schema: Optional[str] = None


class DQConfig(BaseModel):
    global_settings: GlobalSettings
    environments: Dict[str, Environment]

    def get_environment_by_name(self, name: str) -> Optional[Environment]:
        return self.environments.get(name, None)


# TODO: Replace with factory pattern/plugin system. 
# It should be possible to create new environment type config types without modifying this code.
ENV_MAPS = {
    'sqlite':  DatabaseEnvironment,
    'postgres': DatabaseEnvironment,
    'mysql': DatabaseEnvironment,
    'oracle': DatabaseEnvironment,
    'sqlserver': DatabaseEnvironment,
    'clickhouse': DatabaseEnvironment,
    'filesystem': FileSystemEnvironment,
    'sftp': FileSystemEnvironment
}


def create_environment(name: str, env_data: dict) -> Environment:
    env_class = ENV_MAPS.get(env_data['env_type'])
    if env_class:
        return env_class(**env_data)
    else:
        raise ValidationError(f"Unknown environment type: {env_data['env_type']}")


def load_config(config_path: str) -> DQConfig:
    try:
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)
            global_settings = GlobalSettings(**config_data['global_settings'])
            environments = {}

            for name, env_data in config_data.get('environments', {}).items():
                env_obj = create_environment(name, env_data)
                environments[name] = env_obj

            validated_config = DQConfig(
                global_settings=global_settings,
                environments=environments
            )
    except FileNotFoundError:
        raise DQMissingConfigFileError(config_path)
    except (yaml.YAMLError, ValidationError) as e:
        raise DQInvalidConfigFileError(config_path, str(e))
    
    return validated_config 


def load_secrets(file_path: str) -> SecretsFile:
    try:
        with open(file_path, 'r') as file:
            secrets_data = yaml.safe_load(file)
            validated_secrets = SecretsFile(environments=secrets_data)
    except FileNotFoundError:
        raise DQMissingConfigFileError(file_path)
    except (yaml.YAMLError, ValidationError) as e:
        raise DQInvalidConfigFileError(file_path, str(e))
    
    return validated_secrets


def load_config_with_secrets(config_path: str, secrets_path: Optional[str]) -> DQConfig:
    secrets = load_secrets(secrets_path) if secrets_path else SecretsFile(environments={})
    config = load_config(config_path)
    for name, env in config.environments.items():
        env_secrets = secrets.environments.get(name, None)
        if env_secrets:
            env.user = env_secrets.user
            env.password = env_secrets.password
    return config
