from dq.core.config import Environment
from typing import Optional


class ClickhouseHttpEnvironment(Environment):
    path: str
    output_schema: Optional[str] = None

