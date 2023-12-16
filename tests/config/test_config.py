import pytest
import os
import yaml
from dq.core.config import (
    load_config, 
    load_secrets, 
    loaf_config_with_secrets,
    DQConfig, 
    DQMissingConfigFileError, 
    DQInvalidConfigFileError
)

TEST_CONFIG_FILE = 'test_config.yaml'
TEST_SECRETS_FILE = 'test_secrets.yaml'


def get_file_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

# Test for successful config load
def test_load_config():
    config_path = get_file_path(TEST_CONFIG_FILE)
    config = load_config(config_path)
    assert isinstance(config, DQConfig)
    # ... additional assertions ...

# Test for successful secrets load
def test_load_secrets():
    secrets_path = get_file_path(TEST_SECRETS_FILE)
    secrets = load_secrets(secrets_path)
    # ... assertions ...

# Test for successful integration of config and secrets
def test_loaf_config_with_secrets():
    config_path = get_file_path(TEST_CONFIG_FILE)
    secrets_path = get_file_path(TEST_SECRETS_FILE)
    config = loaf_config_with_secrets(config_path, secrets_path)
    # ... assertions ...

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