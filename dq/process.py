import pathlib as pl
import yaml
import pandas as pd
import dq.connection as cn # this is the connection.py file
import re
from dq.test import parse_dq_test_from_yaml, DQTest, Severity, Metric
from typing import List, Optional

# loading queries and tests details from *_test files in plain_sql folder
def process_test_files(file_name:str):
    test_files = pl.Path(file_name).glob('*_test.yaml')
    for test_file in test_files:
        yield process_test_file(test_file)
    

def process_test_file(file_name:str) -> List[DQTest]:
    with open(file_name, 'r') as file:
        content = file.read()

    queries = re.split(r'\n(?=\/\*)', content)
    queries = list(filter(None, queries))

    parsed_queries = []

    for query in queries:
        # Extract the comments
        comments = re.search(r'\/\*(.*?)\*\/', query, re.DOTALL).group(1).rstrip()
        # Extract the query
        query = re.sub(r'\/\*.*?\*\/', '', query, flags=re.DOTALL).strip()
        if query.endswith(';'):
            query = query[:-1].strip()

        dq_test = parse_dq_test_from_yaml(comments)
        dq_test.test_query = query

        parsed_queries.append(dq_test)

    return parsed_queries
