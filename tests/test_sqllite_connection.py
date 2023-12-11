import pytest
import pandas as pd
import sqlite3
from dq.connection import SQLiteConnection  # Replace with the actual module name

@pytest.fixture(scope="module")
def test_db():
    # Setup: Create a temporary SQLite database and table
    test_db_name = 'test.db'
    conn = sqlite3.connect(test_db_name)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
    sample_data = [(1, 'Alice'), (2, 'Bob')]
    cursor.executemany("INSERT INTO test_table VALUES (?, ?)", sample_data)
    conn.commit()

    yield test_db_name  # This value is used in the tests

    # Teardown: Remove the test database and table
    cursor.execute("DROP TABLE test_table")
    conn.commit()
    conn.close()

def test_select_returns_dataframe(test_db):
    connection = SQLiteConnection(database=test_db)
    sql = 'SELECT * FROM test_table'
    result = connection.select(sql)

    assert isinstance(result, pd.DataFrame), "Expected a DataFrame"
    assert len(result) == 2, "Expected 2 rows in the DataFrame"

def test_select_handles_sql_error(test_db):
    connection = SQLiteConnection(database=test_db)
    sql = 'SELECT * FROM non_existent_table'
    
    with pytest.raises(Exception) as excinfo:
        connection.select(sql)
    
    assert 'no such table' in str(excinfo.value), "Expected a 'no such table' error"