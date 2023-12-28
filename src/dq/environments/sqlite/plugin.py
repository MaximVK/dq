from dq.core.plugin import BasePlugin
from dq.environments.sqlite.environment import SQLiteEnvironment
from dq.environments.sqlite.adapter import SQLiteAdapter


class ClickhousePlugin(BasePlugin):
    def adapter_class(self):
        return SQLiteAdapter

    def environment_class(self):
        return SQLiteEnvironment
