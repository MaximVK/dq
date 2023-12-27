from dq.core.dbadapter import TestAbstractAdapter


class SQLiteAdapter(TestAbstractAdapter):

    def saysomething(self):
        print("I'm SQLite!")