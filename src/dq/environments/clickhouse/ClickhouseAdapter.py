from dq.core.dbadapter import TestAbstractAdapter


class ClickhouseAdapter(TestAbstractAdapter):
    def saysomething(self):
        print("I'm clickhouse!")