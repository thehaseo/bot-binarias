﻿import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.pricing as pricing
import pandas as pd
import time
from multiprocessing import Value

"""La siguiente clase se usará exclusivamente para medir el tiempo en el que el módulo SeguimientoRangos se dejará
de ejecutar a través de un cronometro"""
class CronometroEjecucionModulo:
    def __init__(self):
        self.tiempo_de_espera_minutos = Value('i', 0)

    def retornar_cronometro(self):
        return self.tiempo_de_espera_minutos.value

    # Este método siempre se debe de ejecutar a través de un subproceso
    def comenzar_cronometro(self, tiempo_de_espera_minutos):
        self.tiempo_de_espera_minutos.value = tiempo_de_espera_minutos
        time.sleep(int(tiempo_de_espera_minutos) * 60)
        self.tiempo_de_espera_minutos.value = 0


def extraccion_10s_continua(divisa, tiempo_finalizacion, objeto_rango, monto):
    params = {"count": 500, "granularity": "S10"}  # granularity can be in seconds S5 -
    # S30, minutes M1 - M30, hours H1 - H12, days D, weeks W or months M
    client = oandapyV20.API(access_token="e51f5c80499fd16ae7e9ff6676b3c53f-3ac97247f6df3ad7b2b3731a4b1c2dc3",
                            environment="practice")
    account_id = "101-011-12930479-001"
    try:
        candles = instruments.InstrumentsCandles(instrument=divisa, params=params)
        client.request(candles)
        ohlc_dict = candles.response["candles"]
    except Exception as e:
        if e == KeyboardInterrupt:
            return
        print(f"excepcion {e}: {type(e)}")
        print("hubo error, verificar si la ejecucion continua")
        candles = instruments.InstrumentsCandles(instrument=divisa, params=params)
        client.request(candles)
        ohlc_dict = candles.response["candles"]
    ohlc = pd.DataFrame(ohlc_dict)
    datos_10s = ohlc.mid.dropna().apply(pd.Series)
    datos_10s["volume"] = ohlc["volume"]
    datos_10s.index = ohlc["time"]
    datos_10s = datos_10s.apply(pd.to_numeric)
    live_data = []  # precios que recorre el par de divisa en el timeframe seleccionado
    live_price_request = pricing.PricingInfo(accountID=account_id, params={"instruments": divisa})
    rango_precios = []
    cronometro = CronometroEjecucionModulo()
    actual_time = time.time()
    while actual_time < tiempo_finalizacion:
        try:
            starttime = time.time()
            timeout2 = starttime + 10
            while starttime <= timeout2:  # Se cuenta 10 segundos de extraccion de datos para luego filtrar
                live_price_data = client.request(live_price_request)
                live_data.append(live_price_data)
                objeto_rango.seguimiento_precio(live_price_data, divisa, monto, cronometro)
                starttime = time.time()
                time.sleep(1)
            for i in range(len(live_data) - 1):  # Se saca la media entre el Bid y el ask para tener el precio real
                precio = (float(live_data[i]["prices"][0]["closeoutBid"])
                          + float(live_data[i]["prices"][0]["closeoutAsk"])) / 2
                rango_precios.append(precio)
            last_data_row = pd.DataFrame(index=[live_data[-1]["time"]], columns=["o", "h", "l", "c"])
            last_data_row['o'] = round(rango_precios[0], 6)
            last_data_row['h'] = round(max(rango_precios), 6)
            last_data_row['l'] = round(min(rango_precios), 6)
            last_data_row['c'] = round(rango_precios[-1], 6)
            datos_10s = datos_10s.append(last_data_row, sort=False)
            datos_10s = datos_10s.iloc[-500:]
            datos_10s.index.name = "time"
            pd.DataFrame.to_csv(datos_10s, "datos_10s.csv")
            live_data.clear()
            rango_precios.clear()
            actual_time = time.time()
        except Exception as e:
            if e == KeyboardInterrupt:
                return
            print(f"excepcion {e}: {type(e)}")
            print("hubo error, verificar si la ejecucion continua")
            extraccion_10s_continua(divisa, tiempo_finalizacion, objeto_rango, monto)
