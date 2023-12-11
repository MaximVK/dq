import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from datetime import datetime
from typing import List
  

class Validator(ABC):
    @abstractmethod
    def validate_metric(self, value):
        pass

    def is_match(self, condition: str):
        pass

    def to_dict(self):
        return {"condition": self.__class__.__name__, "value": self.check_condition()}


class MoreOrLessValidator(Validator):
    def __init__(self, threshold, direction):
        self.threshold = threshold
        self.direction = direction

    def check_condition(self, value):
        return value <= self.threshold

    def to_dict(self):
        return {"condition": self.__class__.__name__, "threshold": self.threshold}


class ZeroValidator(Validator):
    def check_condition(self, value):
        return value == 0


class RAGValidator(Validator):
    def __init__(self, condition: str):
        vals = condition.split(",")
        self.red   = float(vals[0])
        self.amber = float(vals[1])
        self.green  = float(vals[2])

    def check_condition(self, value):
        if value > self.red:
            return "RED"
        elif value > self.amber:
            return "AMBER"
        elif value > self.green:
            return "GREEN"
        else:
            return "UNKNOWN"

    def is_match(self, condition: str) -> bool:
        return True


    def to_dict(self):
        return {"condition": self.__class__.__name__, "amber": self.amber, "red": self.red}

# TODO: Only RAG Validator is support is supported
def get_validator(condition: str) -> Validator:
    return RAGValidator(condition)
    