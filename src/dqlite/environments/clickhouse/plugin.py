from dqlite.core.plugin import BasePlugin
from dqlite.environments.clickhouse.environment import ClickhouseEnvironment
from dqlite.environments.clickhouse.adapter import ClickhouseAdapter


class ClickhousePlugin(BasePlugin):
    def adapter_class(self):
        return ClickhouseAdapter

    def environment_class(self):
        return ClickhouseEnvironment
