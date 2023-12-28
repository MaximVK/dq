from dqlite.core.dbadapter import BaseDatabaseAdapter
import pandas as pd
from contextlib import contextmanager
from dqlite.environments.clickhouse.environment import ClickhouseEnvironment

class ClickhouseAdapter(BaseDatabaseAdapter):
    def __init__(self, config: ClickhouseEnvironment):
        self.config = config

    @contextmanager
    def _connect(self):
        conn = None
        try:
            yield conn
        finally:
            conn.close()

    def run_test_query(self, test_query:str) -> pd.DataFrame:
        with self._connect() as conn:
            try:
                return pd.read_sql(test_query, conn)
            except Exception as e:
                print(f"An error occurred: {e}")
                #TODO: Additional error handling as required
                raise

    def save_details(self, details:pd.DataFrame, details_table:str) -> None:
        with self._connect() as conn:
            try:
                pass
            #     TODO: Write dataframe logic here
            except Exception as e:
                print(f"An error occurred: {e}")
                #TODO: Additional error handling as required
                raise

    def save_run_results(self, results, results_table:str) -> None:
        raise NotImplementedError
