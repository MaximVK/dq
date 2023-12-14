import pytest
from dq.test_results import TestProcessor
from dq.test import DQTest, Metric
from dq.connection import get_connection
from dq.validators import get_validator
import dq

# Sample DQTest object for testing
@pytest.fixture
def sample_dqtest():
    return DQTest(
        environment="TestEnv",
        test_query="SELECT var1, var2 from table1",
        metrics=[Metric(metric_variable="var1", rag="1,2,3")]
    )

# Mock Configuration
@pytest.fixture
def mock_config(mocker):
    config = mocker.MagicMock()
    config.get_environment_by_name.return_value = mocker.MagicMock()
    return config

def test_process_successful(mocker, mock_config, sample_dqtest):
    print(get_connection)  # Debug: print before patching

    # Mocking get_connection and get_validator
    mock_conn = mocker.MagicMock()
    mock_conn.select.return_value = {"var1": [50]}
    mocker.patch.object(dq.test_results, "get_connection", return_value=mock_conn)
    print(get_connection)  # Debug: print after patching

    print(get_validator)  # Debug: print after patching
    mock_validator = mocker.MagicMock()
    mock_validator.validate_metric.return_value = "GREEN"
    mocker.patch.object(dq.validators, "get_validator", return_value=mock_validator)
    print(get_validator)  # Debug: print after patching
    print(get_validator("1,2,3"))  # Debug: print after patching


    processor = TestProcessor(config=mock_config)

    # Process the test
    result = next(processor.process([sample_dqtest]))

    # Assertions
    assert result.environment == "TestEnv"
    assert result.test_status == "GREEN"


def test_process_exception(mocker, mock_config, sample_dqtest):
    # Mocking exception in get_connection
    mocker.patch("dq.connection.get_connection", side_effect=Exception("DB Connection Failed"))

    processor = TestProcessor(config=mock_config)

    # Process the test
    result = next(processor.process([sample_dqtest]))

    # Assertions
    assert result.execution_status == "FAILED"
    assert result.exception == "DB Connection Failed"
    # ... other assertions ...