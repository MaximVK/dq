
# @dqlite.test("R1", "RMS Trades", "Number of missing trades", RAG(10, 20, 30),
#          "Number of missing trades should be less than 10% of total trades")
# def dqtest_number_of_missing_trades(dqlite):
#     dqlite.execute("select count(1) from rms.trade")
#     if dqlite.metric_value > 0:
#         dqlite.execute_details("select systemid, structureid, tradedate from rms.trade where ...")
#     dqlite.assert_metric_value()
#
#

