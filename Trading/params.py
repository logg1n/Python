class Params:
    Param_TakeProfit = 0.007
    Param_StopLoss = 0.01
    Param_OpenPosition = 0.0
    # Param_Comission =
    Param_Interval = 5
    Param_Squeeze = 1.0
    Param_HighVolatilityPrcnt = 2.5 / 100
    Param_LowVolatilityPrcnt = 1.3 / 100

    class Side:
        Sell = "Sell"
        Buy = "Buy"
        TP = "tp"
        SL = "sl"
