import pandas as pd
from contextlib import contextmanager
from dq.core.config import Environment
import logging


class Connection:
    @contextmanager
    def _connect(self):
        # This method should be overridden to provide the correct connection
        raise NotImplementedError

    def select(self, sql: str, params=None) -> pd.DataFrame:
        with self._connect() as conn:
            try:
                return pd.read_sql(sql, conn, params=params)
            except Exception as e:
                print(f"An error occurred: {e}")
                # Additional error handling as required
    
    def save_details(self, sql: str, params=None) -> pd.DataFrame:
        with self._connect() as conn:
            try:
                return pd.read_sql(sql, conn, params=params)
            except Exception as e:
                print(f"An error occurred: {e}")
                # Additional error handling as required

        
    