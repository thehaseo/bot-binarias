import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import pandas as pd
import time
import oandapyV20.endpoints.pricing as pricing
from analisis_y_estrategia import analisis_estrategia, ejecucion
import fxcmpy
from multiprocessing import Process


class ExtraccionFxcmpy(Process):
    def __init__(self, numero_de_velas, timeframe, par_de_divisas):
        super().__init__()

        self.numero_de_velas = numero_de_velas
        self.timeframe = timeframe
        self.par_de_divisas = par_de_divisas

    def run(self):
        self.conexion = fxcmpy.fxcmpy(access_token="a962060d184b5fbe05ad48e1ba9be1b846548a6f", log_level='error',
                                      server='demo')
        temporalidad = (60 if (self.timeframe == "m1") else
                        300 if (self.timeframe == "m5") else
                        600 if (self.timeframe == "m10") else
                        900 if (self.timeframe == "m15") else
                        1800 if (self.timeframe == "m30") else
                        3600 if (self.timeframe == "H1") else
                        0)
        while True:
            starttime = time.time()
            data = self.conexion.get_candles(self.par_de_divisas, period=self.timeframe, number=self.numero_de_velas)
            data.apply(pd.to_numeric)
            ohlc_df = pd.DataFrame()
            ohlc_df["o"] = (data.loc[:, "bidopen"] + data.loc[:, "askhigh"]) / 2
            ohlc_df["h"] = (data.loc[:, "bidhigh"] + data.loc[:, "askhigh"]) / 2
            ohlc_df["l"] = (data.loc[:, "bidlow"] + data.loc[:, "asklow"]) / 2
            ohlc_df["c"] = (data.loc[:, "bidclose"] + data.loc[:, "askclose"]) / 2
            ohlc_df["resistencia"] = ohlc_df["h"].rolling(20).max()
            ohlc_df["soporte"] = ohlc_df["l"].rolling(20).min()
            pd.DataFrame.to_csv(ohlc_df, f"datos {self.timeframe}")
            time.sleep(temporalidad - ((time.time() - starttime) % temporalidad))
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           