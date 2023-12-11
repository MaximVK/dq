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


class RAGCondition(Validator):
    def __init__(self, amber, red):
        self.amber = amber
        self.red = red

    def check_condition(self, value):
        if value > self.red:
            return "Red"
        elif value > self.amber:
            return "Amber"
        else:
            return "Green"

    def to_dict(self):
        return {"condition": self.__class__.__name__, "amber": self.amber, "red": self.red}

