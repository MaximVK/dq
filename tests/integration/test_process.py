import sqlite3
from pathlib import Path
import pytest
import os
from logger_config import logger
from dq.core.config import load_config_with_secrets, DQConfig
from dq.process import process_test_file
from dq.test_results import DQTestProcessor   

def get_file_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

@pytest.fixture(scope="module")
def module_tmp_path(tmp_path_factory):
    return tmp_path_factory.mktemp("data")

# Fixture to create an SQLite database file
@pytest.fixture(scope="module")
def sqlite_db_file(module_tmp_path: Path):
    logger.info("Creating SQLite database") 
    path_to_db = module_tmp_path / "testdb.db"
    conn = sqlite3.connect(path_to_db)

    c = conn.cursor()

    # Create table1
    c.execute('''
        CREATE TABLE departments (
            department_id INTEGER PRIMARY KEY,
            department_name TEXT
        )
    ''')

    # Create table2
    c.execute('''
        CREATE TABLE jobs (
            job_id INTEGER PRIMARY KEY,
            job_title TEXT,
            min_salary INTEGER,
            max_salary INTEGER
        )
    ''')

    # Create table3
    c.execute('''
        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            hire_date TEXT,
            department_id INTEGER,
            job_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments (department_id),
            FOREIGN KEY (job_id) REFERENCES jobs (job_id)
        )
    ''')

    # Insert data into departments (with duplicates)
    departments = [(1, 'Human Resources'),
                   (2, 'Engineering'),
                   (3, 'Marketing'),
                   (4, 'Sales'),
                   (5, 'Sales')]  # Duplicate department
    c.executemany('INSERT INTO departments VALUES (?,?)', departments)

    # Insert data into jobs (with anomaly: negative salary)
    jobs = [(1, 'Manager', 60000, 80000),
            (2, 'Engineer', 70000, 90000),
            (3, 'Sales Representative', 40000, 60000),
            (4, 'Marketing Manager', -50000, 70000), # Anomaly: Negative min_salary
            (5, 'Sales Manager', 50000, 700000) # Anomaly: Max salary seems to high
            ]
      
    c.executemany('INSERT INTO jobs VALUES (?,?,?,?)', jobs)

    # Insert data into employees (with missing values: NULL department_id and job_id)
    employees = [(1, 'John', 'Doe', '2023-07-01', 1, 1),
                 (2, 'Jane', 'Smith', '2023-07-02', 2, 2),
                 (3, 'Robert', 'Johnson', '2023-07-03', None, 3),  # Missing department_id
                 (4, 'Michael', 'Williams', '2023-07-04', 4, None),  # Missing job_id
                 (5, 'William', 'Brown', '2023-07-05', None, None)]  # Missing department_id and job_id
    c.executemany('INSERT INTO employees VALUES (?,?,?,?,?,?)', employees)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return str(path_to_db)


@pytest.fixture(scope="module")
def secrets_file(module_tmp_path: Path):
    secrets_data = """
    environment_name:
      user: test_user
      password: test_password
    """
    secrets_file = module_tmp_path / "secrets.yml"
    secrets_file.write_text(secrets_data)
    return str(secrets_file)


@pytest.fixture(scope="module")
def config_file(module_tmp_path: Path, sqlite_db_file: str):
    config_data = f"""
    global_settings:
        default_output_env: TestDB 
    evnironments:
      TestDB:
        conn: sqlite
        path: {sqlite_db_file}
    """
    config_file = module_tmp_path / "config.yml"
    config_file.write_text(config_data)
    return str(config_file)

def test_dq_tests_run(config_file: str, secrets_file: str, sqlite_db_file: str):
    config = load_config_with_secrets(config_file, secrets_file)
    file_path = get_file_path("test_queries.sql")   
    dq_tests = process_test_file(file_path)

    # Process the test
    processor = DQTestProcessor(config=config)
    results = processor.process(dq_tests)

    for result in results:
        logger.info("Test Status:" + result.test_status)
        logger.info("Execution Status:" + result.execution_status)
        logger.info("Exception:" + result.exception)
        logger.info("Environment:" + result.environment)
        logger.info("Host:" + result.host)
        logger.info("User:" + result.user)
        logger.info("Test:" + str(result.test))
        logger.info("Metric Results:" + str(result.metric_results))
        logger.info("Start Timestamp:" + str(result.start_timestamp))
        logger.info("End Timestamp:" + str(result.end_timestamp))
        logger.info("Duration:" + str(result.duration_ms))
        logger.info("--------------------------------------------------")   


