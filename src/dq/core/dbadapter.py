import pandas as pd
from contextlib import contextmanager

from abc import ABC, abstractmethod

class TestAbstractAdapter(ABC):
    @abstractmethod
    def saysomething(self):
        pass

class BaseDatabaseAdapter(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def query(self, query_string):
        pass


class Connection:
    @contextmanager
    def _connect(self):
        # This method should be overridden to provide the correct connection
        raise NotImplementedError

    def _execute_sql(self, sql: str, params=None) -> pd.DataFrame:
        with self._connect() as conn:
            try:
                return pd.read_sql(sql, conn, params=params)
            except Exception as e:
                print(f"An error occurred: {e}")
                # Additional error handling as required

    def select(self, sql: str, params=None) -> pd.DataFrame:
        return self._execute_sql(sql, params)

    def save_details(self, sql: str, params=None) -> None:
        self._execute_sql(sql, params)
        
    