from dqlite.core.plugin import BasePlugin
from dqlite.environments.clickhouse_http.environment import ClickhouseHttpEnvironment
from dqlite.environments.clickhouse_http.adapter import ClickhouseHttpAdapter


class ClickhouseHttpPlugin(BasePlugin):
    def adapter_class(self):
        return ClickhouseHttpAdapter

    def environment_class(self):
        return ClickhouseHttpEnvironment
