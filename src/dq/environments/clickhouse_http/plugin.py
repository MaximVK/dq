from dq.core.plugin import BasePlugin
from dq.environments.clickhouse_http.environment import ClickhouseHttpEnvironment
from dq.environments.clickhouse_http.adapter import ClickhouseHttpAdapter


class ClickhousePlugin(BasePlugin):
    def adapter_class(self):
        return ClickhouseHttpAdapter

    def environment_class(self):
        return ClickhouseHttpEnvironment
