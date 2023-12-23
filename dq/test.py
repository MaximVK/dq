from typing import List, Optional
from enum import Enum
from pydantic import BaseModel
from pydantic import ValidationError
import yaml 
import functools

@functools.total_ordering
class Severity(Enum):
    LOW = 1, 'Low'
    MEDIUM = 2, 'Medium'
    HIGH = 3, 'High'
    CRITICAL = 4, 'Critical'

    def __init__(self, num, label):
        self._num = num
        self._label = label

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self._num < other._num
        return NotImplemented

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self._num == other._num
        return NotImplemented

    def __str__(self):
        return self._label


class Metric(BaseModel):
    metric_variable: str
    description: Optional[str] = None
    rag: str


class DQTest(BaseModel):
    dataset_group: Optional[str] = None
    dataset: Optional[str] = None
    test_name: Optional[str] = None
    environment: str 
    labels: Optional[List[str]] = None
    metrics: List[Metric]
    severity: Severity = Severity.LOW
    test_query: Optional[str] = None 
    details_query: Optional[str] = None


def parse_dq_test_from_yaml(data: str) -> DQTest:
    try:
        yaml_data = yaml.safe_load(data)
        dq_test = DQTest(**yaml_data)
        return dq_test
    except yaml.YAMLError as e:
        raise ValueError("Invalid YAML content: " + str(e))
    except ValidationError as e:
        error_messages = "; ".join([f"{error['loc'][0]}: {error['msg']}" for error in e.errors()])
        raise ValueError("Data validation error for DQTest: " + error_messages)
