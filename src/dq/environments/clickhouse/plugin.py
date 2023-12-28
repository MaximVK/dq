from dq.core.plugin import BasePlugin
from dq.environments.clickhouse.environment import ClickhouseEnvironment
from dq.environments.clickhouse.adapter import ClickhouseAdapter


class ClickhousePlugin(BasePlugin):
    def adapter_class(self):
        return ClickhouseAdapter

    def environment_class(self):
        return ClickhouseEnvironment
