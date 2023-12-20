# Dev How To

## Starting 

```commandline
python3.12 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements
```

## Linting / Type Checking

Do before commit:

```commandline
ruff . --fix
pyright .
```

# Requirements

- It should be possible to run tests locally and on a server with minninal changes in the config file
    - It should be possible to specify configs for uat, staging and production environments
    - It should be possible to specify a personcal developer schema for output when running locally
  
    
