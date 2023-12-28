from dqlite.core.config import Environment
from typing import Optional, Dict, Any


class ClickhouseEnvironment(Environment):
    driver: Optional[str] = None
    host: str = 'localhost'
    port: Optional[int] = None
    user: Optional[str] = 'default'
    retries: int = 1
    database: Optional[str] = ''
    # schema: Optional[str] = 'default'
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
