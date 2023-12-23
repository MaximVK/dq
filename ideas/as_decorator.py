
@dq.test("R1", "RMS Trades", "Number of missing trades", RAG(10, 20, 30),
         "Number of missing trades should be less than 10% of total trades")
def dqtest_number_of_missing_trades(dq):
    dq.execute("select count(1) from rms.trade")
    if dq.metric_value > 0:
        dq.execute_details("select systemid, structureid, tradedate from rms.trade where ...")
    dq.assert_metric_value()



