import pytest
import yaml
from dq.test import parse_dq_test_from_yaml, DQTest, Severity, Metric

def test_parse_valid_yaml():
    # Arrange
    valid_yaml_content = """
    dataset_group: group1
    dataset: dataset1
    test_name: test1
    environment: production
    labels: [label1, label2]
    metrics:
      - metric_variable: metric1
        description: Description 1
        rag: green
      - metric_variable: metric2
        rag: red
    severity: High
    test_query: SELECT * FROM table
    details_query: SELECT details FROM table
    """
    expected_metrics = [
        Metric(metric_variable="metric1", description="Description 1", rag="green"),
        Metric(metric_variable="metric2", rag="red")
    ]

    # Act
    result = parse_dq_test_from_yaml(valid_yaml_content)

    # Assert
    assert isinstance(result, DQTest)
    assert result.dataset_group == "group1"
    assert result.environment == "production"
    assert result.severity == Severity.HIGH
    assert result.metrics == expected_metrics
    assert result.test_query == "SELECT * FROM table"
    assert result.details_query == "SELECT details FROM table"


def test_parse_valid_yaml2():
    valid_yaml_content = """
    dataset_group: "group1"
    dataset: "dataset1"
    environment: "production"
    metrics:
      - metric_variable: "metric1"
        description: "Description 1"
        rag: "green"
    severity: "High"
    """
    result = parse_dq_test_from_yaml(valid_yaml_content)

    assert isinstance(result, DQTest)
    assert result.environment == "production"
    assert result.severity == Severity.HIGH
    assert len(result.metrics) == 1
    assert result.metrics[0].metric_variable == "metric1"

@pytest.mark.parametrize("invalid_yaml, expected_message", [
    ("invalid: \n : yaml: content", "Invalid YAML content"), 
])
def test_parse_invalid_yaml(invalid_yaml, expected_message):
    with pytest.raises(ValueError) as exc_info:
        parse_dq_test_from_yaml(invalid_yaml)
    assert expected_message in str(exc_info.value)

@pytest.mark.parametrize("incomplete_yaml, expected_message_part", [
    ("environment: production\nmetrics: invalid", "metrics: value is not a valid list"),
])
def test_data_validation_errors(incomplete_yaml, expected_message_part):
    with pytest.raises(ValueError) as exc_info:
        parse_dq_test_from_yaml(incomplete_yaml)
    assert expected_message_part in str(exc_info.value)


    