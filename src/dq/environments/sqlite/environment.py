from dq.core.config import Environment
from typing import Optional


class SQLiteEnvironment(Environment):
    path: str
    output_schema: Optional[str] = None

