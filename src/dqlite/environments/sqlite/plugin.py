from dqlite.core.plugin import BasePlugin
from dqlite.environments.sqlite.environment import SQLiteEnvironment
from dqlite.environments.sqlite.adapter import SQLiteAdapter


class SQLitePlugin(BasePlugin):
    def adapter_class(self):
        return SQLiteAdapter

    def environment_class(self):
        return SQLiteEnvironment
