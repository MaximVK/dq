import pandas as pd
from contextlib import contextmanager
from dq.core.config import Environment
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
                raise

class SQLiteConnection(Connection):  
    def __init__(self, database: str):
        self.database = database

    @contextmanager
    def _connect(self):
        import sqlite3
        conn = sqlite3.connect(self.database)
        try:
            yield conn
        finally:
            conn.close()

class SQLServerConnection(Connection):
    def __init__(self, server: str, port: int, database: str, user: str, password: str):
        self.server = server
        self.database = database
        self.user = user
        self.password = password

    @contextmanager
    def _connect(self):
        import pyodbc
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.user};PWD={self.password}'
        conn = pyodbc.connect(conn_str)
        try:
            yield conn
        finally:
            conn.close()

class PostgresConnection(Connection):
    def __init__(self, server: str, port: int, database: str, user: str, password: str):
        self.server = server
        self.database = database
        self.user = user
        self.password = password

    @contextmanager
    def _connect(self):
        import psycopg2
        conn = psycopg2.connect(host=self.server, database=self.database, user=self.user, password=self.password)
        try:
            yield conn
        finally:
            conn.close()

class MySQLConnection(Connection):
    def __init__(self, server: str, port: int, database: str, user: str, password: str):
        self.server = server
        self.database = database
        self.user = user
        self.password = password

    @contextmanager
    def _connect(self):
        import mysql.connector
        conn = mysql.connector.connect(host=self.server, database=self.database, user=self.user, password=self.password)
        try:
            yield conn
        finally:
            conn.close()

class OracleConnection(Connection):
    def __init__(self, server: str, port: int, database: str, user: str, password: str, service_name: str = None, dsn: str = None):
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.service_name = service_name
        self.dsn = dsn or f'{self.server}/{self.database}'

    @contextmanager
    def _connect(self):
        import cx_Oracle
        dsn_str = self.dsn if self.dsn else cx_Oracle.makedsn(self.server, self.database, service_name=self.service_name)
        conn = cx_Oracle.connect(self.user, self.password, dsn_str)
        try:
            yield conn
        finally:
            conn.close()


def get_connection(env: Environment) -> Connection:
    
    if env.conn == 'sqlite':
        logger.info("SQLiteConnection:" + env.path)
        return SQLiteConnection(env.path)
    elif env.conn == 'sqlserver':
        return SQLServerConnection(env.host, env.port, env.database, env.user, env.password)
    elif env.conn == 'postgres':
        return PostgresConnection(env.host, env.port, env.database, env.user, env.password)
    elif env.conn == 'mysql':
        return MySQLConnection(env.host, env.port, env.database, env.user, env.password)
    elif env.conn == 'oracle':
        return OracleConnection(env.host, env.port, env.database, env.user, env.password)
    else:
        raise ValueError(f'Environment type {env.conn} not supported')