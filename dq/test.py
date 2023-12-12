from typing import List, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from pydantic import ValidationError
import yaml 

class Severity(Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    CRITICAL = 'Critical'


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




class MetricResult(BaseModel):
    metric: Metric
    metric_value: float
    rag_status: str


class DQTestResult(BaseModel):
    environment: str
    host: str
    user: str
    status: str
    exception: str
    test: DQTest
    metric_results: List[MetricResult]
    start_timestamp: datetime
    end_timestamp: datetime
    duration: float



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
