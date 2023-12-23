import pytest
from dq.test_results import DQTestProcessor
from dq.test import DQTest, Metric
from dq.connection import get_connection
import dq


# Sample DQTest object for testing
@pytest.fixture
def sample_dqtest() -> DQTest:
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

    mock_validator = mocker.MagicMock()
    mock_validator.validate_metric.return_value = "GREEN"
    mocker.patch.object(dq.test_results, "get_validator", return_value=mock_validator)

    processor = DQTestProcessor(config=mock_config)
    test_run = processor.process([sample_dqtest])
    test_results_iterator = iter(test_run.test_results)

    # Process the test
    result = next(test_results_iterator)

    # Assertions
    assert result.environment == "TestEnv"
    assert result.test_status == "GREEN"


def test_process_exception(mocker, mock_config, sample_dqtest):
    # Mocking exception in get_connection
    mocker.patch.object(dq.test_results, "get_connection", side_effect=Exception("DB Connection Failed"))

    processor = DQTestProcessor(config=mock_config)
    test_run = processor.process([sample_dqtest])
    test_results_iterator = iter(test_run.test_results)

    # Process the test
    result = next(test_results_iterator)

    # Assertions
    assert result.execution_status == "FAILED"
    assert result.exception == "DB Connection Failed"
    # ... other assertions ...
