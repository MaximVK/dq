import pytest
import pandas as pd
import sqlite3
from logger_config import logger
from dq.connection import SQLiteConnection  # Replace with the actual module name


@pytest.fixture(scope="module")
def module_tmp_path(tmp_path_factory):
    return tmp_path_factory.mktemp("data")


@pytest.fixture(scope="module")
def sqlite_db_file(module_tmp_path):
    # Setup: Create a temporary SQLite database and table
    logger.info("Creating SQLite database") 
    path_to_db = module_tmp_path / "testdb.db"
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
    sample_data = [(1, 'Alice'), (2, 'Bob')]
    cursor.executemany("INSERT INTO test_table VALUES (?, ?)", sample_data)
    conn.commit()

    yield path_to_db  

    # Teardown: Remove the test database and table
    cursor.execute("DROP TABLE test_table")
    conn.commit()
    conn.close()


def test_select_returns_dataframe(sqlite_db_file):
    connection = SQLiteConnection(database=str(sqlite_db_file))
    sql = 'SELECT * FROM test_table'
    result = connection.select(sql)

    assert isinstance(result, pd.DataFrame), "Expected a DataFrame"
    assert len(result) == 2, "Expected 2 rows in the DataFrame"


def test_select_handles_sql_error(sqlite_db_file):
    connection = SQLiteConnection(database=str(sqlite_db_file))
    sql = 'SELECT * FROM non_existent_table'
    
    with pytest.raises(Exception) as excinfo:
        connection.select(sql)
    
    assert 'no such table' in str(excinfo.value), "Expected a 'no such table' error"
