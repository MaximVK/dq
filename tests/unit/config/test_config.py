import pytest
import os
import yaml
from dqlite.core.config import (
    load_config, 
    load_secrets, 
    load_config_with_secrets,
    DQConfig, 
    DQMissingConfigFileError, 
    DQInvalidConfigFileError,
    GlobalSettings,
    DatabaseEnvironment,
    FileSystemEnvironment,
    EnvironmentCredentials,
    SecretsFile
)

TEST_CONFIG_FILE = 'test_config.yaml'
TEST_SECRETS_FILE = 'test_secrets.yaml'


def get_file_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


# Test for successful config load
def test_load_config():
    config_path = get_file_path(TEST_CONFIG_FILE)
    config = load_config(config_path)

    # Basic checks
    assert isinstance(config, DQConfig)
    assert isinstance(config.global_settings, GlobalSettings)
    assert isinstance(config.environments, dict)

    # Check global settings
    assert config.global_settings.default_output_env == "TestDB"

    # Check specific environments
    assert "TestDB" in config.environments
    testdb = config.environments["TestDB"]
    assert isinstance(testdb, DatabaseEnvironment)
    assert testdb.name == "TestDB"
    assert testdb.env_type == "sqlite"
    assert testdb.is_output
    assert testdb.path == "/data/TestDB.sqlite"
    assert testdb.database == "TestDB"
    assert testdb.host == "localhost"
    assert testdb.port == 5432

    assert "LocalFS" in config.environments
    local_fs = config.environments["LocalFS"]
    assert isinstance(local_fs, FileSystemEnvironment)
    assert local_fs.name == "LocalFS"
    assert local_fs.env_type == "filesystem"
    assert local_fs.is_output
    assert local_fs.path == "/mnt/local_storage"
    assert local_fs.output_folder == "/mnt/local_storage/output"

# Test for successful secrets load
def test_load_secrets():
    secrets_path = get_file_path(TEST_SECRETS_FILE)
    secrets = load_secrets(secrets_path)

    # Basic checks
    assert isinstance(secrets, SecretsFile)
    assert isinstance(secrets.environments, dict)

    assert "TestDB" in secrets.environments
    testdb_creds = secrets.environments["TestDB"]
    assert isinstance(testdb_creds, EnvironmentCredentials)
    assert testdb_creds.user == "test_user"
    assert testdb_creds.password.get_secret_value() == "test_password"


# Test for successful integration of config and secrets
def test_load_config_with_secrets():
    config_path = get_file_path(TEST_CONFIG_FILE)
    secrets_path = get_file_path(TEST_SECRETS_FILE)
    config = load_config_with_secrets(config_path, secrets_path)

    assert isinstance(config, DQConfig)

    testdb = config.environments["TestDB"]
    assert testdb.user == "test_user"
    assert testdb.password.get_secret_value() == "test_password"


# Test for missing config file
def test_missing_config_file():
    with pytest.raises(DQMissingConfigFileError):
        load_config(get_file_path('nonexistent_config.yaml'))


# Test for missing secrets file
def test_missing_secrets_file():
    with pytest.raises(DQMissingConfigFileError):
        load_secrets(get_file_path('nonexistent_secrets.yaml'))


# Test for invalid config file format
def test_invalid_config_format(mocker):
    mocker.patch('builtins.open', mocker.mock_open(read_data="invalid content"))
    mocker.patch('yaml.safe_load', side_effect=yaml.YAMLError("Error parsing YAML"))
    with pytest.raises(DQInvalidConfigFileError):
        load_config(get_file_path('invalid_config.yaml'))


# Test for invalid secrets file format
def test_invalid_secrets_format(mocker):
    mocker.patch('builtins.open', mocker.mock_open(read_data="invalid content"))
    mocker.patch('yaml.safe_load', side_effect=yaml.YAMLError("Error parsing YAML"))
    with pytest.raises(DQInvalidConfigFileError):
        load_secrets(get_file_path('invalid_secrets.yaml'))