from dq.core.dbadapter import BaseDatabaseAdapter
from dq.core.config import Environment
from typing import Optional, Dict, Any
import pandas as pd
from contextlib import contextmanager

class ClickhouseConfig(Environment):
    driver: Optional[str] = None
    host: str = 'localhost'
    port: Optional[int] = None
    user: Optional[str] = 'default'
    retries: int = 1
    database: Optional[str] = ''
    schema: Optional[str] = 'default'
    password: str = ''
    cluster: Optional[str] = None
    database_engine: Optional[str] = None
    cluster_mode: bool = False
    secure: bool = False
    verify: bool = True
    connect_timeout: int = 10
    send_receive_timeout: int = 300
    sync_request_timeout: int = 5
    compress_block_size: int = 1048576
    compression: str = ''
    check_exchange: bool = True
    custom_settings: Optional[Dict[str, Any]] = None
    use_lw_deletes: bool = False
    local_suffix: str = 'local'
    allow_automatic_deduplication: bool = False

class ClickhouseAdapter(BaseDatabaseAdapter):
    def __init__(self, config: ClickhouseConfig):
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
