from random import randint

from dq.report import Table
from dq.report.model import *
from dq.report.report_generator import generate_html_report


def test_table():
    t = Table(columns=[Table.Column()], rows=[["1"]])
    res = t.render()
    print(res)