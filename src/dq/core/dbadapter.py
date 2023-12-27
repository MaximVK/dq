import pandas as pd
from contextlib import contextmanager
from abc import ABC, abstractmethod


class BaseDatabaseAdapter(ABC):
    @abstractmethod
    def run_test_query(self, test_query:str) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def save_details(self, details:pd.DataFrame) -> None:
        raise NotImplementedError

    @abstractmethod
    def save_run_results(self, results) -> None:
        raise NotImplementedError

# class Connection:
#     @contextmanager
#     def _connect(self):
#         # This method should be overridden to provide the correct connection
#         raise NotImplementedError
#
#     def _execute_sql(self, sql: str, params=None) -> pd.DataFrame:
#         with self._connect() as conn:
#             try:
#                 return pd.read_sql(sql, conn, params=params)
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#                 # Additional error handling as required
#
#     def select(self, sql: str, params=None) -> pd.DataFrame:
#         return self._execute_sql(sql, params)
#
#     def save_details(self, sql: str, params=None) -> None:
#         self._execute_sql(sql, params)
#
    