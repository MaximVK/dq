import pathlib as pl
import yaml
import pandas as pd
import dq.connection as cn # this is the connection.py file
import re


# loading queries and tests details from *_test files in plain_sql folder
def process_test_files(file_name:str):
    test_files = pl.Path(file_name).glob('*_test.yaml')
    for test_file in test_files:
        yield process_test_file(test_file)
    

def process_test_file(file_name:str):
    with open(file_name, 'r') as file:
        content = file.read()

    # Split the content into individual SQL queries
    queries = re.split(r'\n(?=\/\*)', content)

    # Remove empty strings from the list of queries
    queries = list(filter(None, queries))

    parsed_queries = []

    # Parse each query and create an object
    for query in queries:
        # Extract the comments
        comments = re.search(r'\/\*(.*?)\*\/', query, re.DOTALL).group(1).rstrip()

        # Parse the comments section as YAML
        comments_yaml = yaml.safe_load(comments)

        # Remove comments from the query string
        query = re.sub(r'\/\*.*?\*\/', '', query, flags=re.DOTALL).strip()

        # Remove the semicolon from the end of the query, if present
        if query.endswith(';'):
            query = query[:-1].strip()

        # Create an object with comments and SQL query attributes
        query_object = {
            'comments': comments_yaml,
            'sql_query': query
        }

        # Append the object to the list
        parsed_queries.append(query_object)

    return parsed_queries
