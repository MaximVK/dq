import pytest
import yaml
from dq.config import Environment, Configuration, load_config, load_secrets

def test_load_config(tmp_path):
    # Create a temporary YAML file for testing
    yaml_file_path = tmp_path / "test_config.yaml"
    with open(yaml_file_path, 'w') as temp_file:
        yaml_data = """
        Environments:
          TestDB:
            conn: sqlite
            path: plain_sql/TestDB.sqlite
          FinanceDB:
            conn: postgres
            host: localhost
            port: 5432
            user: postgres
            password: postgres
            database: finance
        """
        temp_file.write(yaml_data)

    # Create a temporary secrets YAML file for testing
    secrets_file_path = tmp_path / "test_secrets.yaml"
    with open(secrets_file_path, 'w') as temp_file:
        secrets_data = """
        TestDB:
          user: test_user
          password: test_password
        """
        temp_file.write(secrets_data)

    config = load_config(yaml_file_path, secrets_file_path)
    assert isinstance(config, Configuration)
    assert len(config.environments) == 2

    # Test getting environments by name
    test_db = config.get_environment_by_name('TestDB')
    finance_db = config.get_environment_by_name('FinanceDB')
    assert isinstance(test_db, Environment)
    assert isinstance(finance_db, Environment)
    assert test_db.name == 'TestDB'
    assert finance_db.name == 'FinanceDB'

    # Test environment attributes
    assert test_db.conn == 'sqlite'
    assert test_db.path == 'plain_sql/TestDB.sqlite'
    assert test_db.user == 'test_user'  # Loaded from secrets
    assert test_db.password == 'test_password'  # Loaded from secrets
    assert test_db.host is None  # No host in the YAML
    assert finance_db.conn == 'postgres'
    assert finance_db.host == 'localhost'
    assert finance_db.port == 5432
    assert finance_db.user == 'postgres'
    assert finance_db.password == 'postgres'
    assert finance_db.database == 'finance'

def test_load_secrets(tmp_path):
    # Create a temporary secrets YAML file for testing
    secrets_file_path = tmp_path / "test_secrets.yaml"
    with open(secrets_file_path, 'w') as temp_file:
        secrets_data = """
        TestDB:
          user: test_user
          password: test_password
        """
        temp_file.write(secrets_data)

    secrets = load_secrets(secrets_file_path)
    assert isinstance(secrets, dict)
    assert 'TestDB' in secrets
    assert 'FinanceDB' not in secrets  # FinanceDB is not in the secrets file
    assert secrets['TestDB']['user'] == 'test_user'
    assert secrets['TestDB']['password'] == 'test_password'

def test_load_config_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        non_existent_yaml_file = tmp_path / "non_existent_config.yaml"
        load_config(str(non_existent_yaml_file))

def test_load_config_yaml_error(tmp_path):
    # Create a temporary YAML file with invalid syntax
    invalid_yaml_file = tmp_path / "invalid_config.yaml"
    with open(invalid_yaml_file, 'w') as temp_file:
        temp_file.write("invalid_yaml_data")

    with pytest.raises(ValueError):
        load_config(str(invalid_yaml_file))

def test_load_secrets_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        non_existent_secrets_file = tmp_path / "non_existent_secrets.yaml"
        load_secrets(str(non_existent_secrets_file))

@pytest.mark.skip(reason="Not implemented yet")
def test_load_secrets_yaml_error(tmp_path):
    # Create a temporary YAML file with invalid syntax
    invalid_yaml_file = tmp_path / "invalid_secrets.yaml"
    with open(invalid_yaml_file, 'w') as temp_file:
        temp_file.write("invalid_yaml_data")

    with pytest.raises(ValueError):
        load_secrets(str(invalid_yaml_file))
