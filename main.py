from ExtraccionDatosOanda import ExtraccionOanda
from analisis_y_estrategia import analisis_y_estrategia1, analisis_y_estrategia2, analisis_y_estrategia3
from Ejecucion import ejecucion
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.pricing as pricing
import time
import pandas as pd


def run(tiempo_de_ejecucion_minutos, primera_divisa, segunda_divisa, estrategia, numero_noticias, horas_noticias):
    print("comenzando")
    timeout = time.time() + (tiempo_de_ejecucion_minutos * 60)
    divisa = f"{primera_divisa}_{segunda_divisa}"
    proceso_1_min = ExtraccionOanda(500, "M1", f"{primera_divisa}_{segunda_divisa}")
    proceso_5_min = ExtraccionOanda(120, "M5", f"{primera_divisa}_{segunda_divisa}")
    proceso_1_min.start()
    proceso_5_min.start()
    time.sleep(30)
    datos_1min = pd.read_csv("datos_M1.csv", index_col="time")
    resistencia_mayor_1m = datos_1min["h"].rolling(150).max().dropna()
    resistencia_menor_1m = datos_1min["c"].rolling(150).max().dropna()
    resistencia_punto_mayor_1m = resistencia_mayor_1m.iloc[-1]
    resistencia_punto_menor_1m = resistencia_menor_1m.iloc[-1]
    # Se calcula rango de resistencia en las últimas 150 velas a 1 minuto
    for data in range(-150, 0):
        precio_h = datos_1min['h'].iloc[data]
        precio_o = datos_1min['o'].iloc[data]
        precio_c = datos_1min['c'].iloc[data]
        if precio_h > resistencia_punto_menor_1m > precio_c:
            if precio_c >= precio_o:
                resistencia_punto_menor_1m = precio_c
            elif precio_c < precio_o < resistencia_punto_menor_1m:
                resistencia_punto_menor_1m = precio_o
    soporte_menor_1m = datos_1min["l"].rolling(150).min().dropna()
    soporte_mayor_1m = datos_1min["c"].rolling(150).min().dropna()
    soporte_punto_menor_1m = soporte_menor_1m.iloc[-1]
    soporte_punto_mayor_1m = soporte_mayor_1m.iloc[-1]
    # Se calcula rango de soporte en las últimas 150 velas a 1 minuto
    for data in range(-50, 0):
        precio_l = datos_1min['l'].iloc[data]
        precio_o = datos_1min['o'].iloc[data]
        precio_c = datos_1min['c'].iloc[data]
        if precio_l < soporte_punto_mayor_1m < precio_c:
            if precio_c <= precio_o:
                soporte_punto_mayor_1m = precio_c
            elif precio_c > precio_o > soporte_punto_mayor_1m:
                soporte_punto_mayor_1m = precio_o
    datos_5min = pd.read_csv("datos_M5.csv", index_col="time")
    resistencia_mayor_5m = datos_5min["h"].rolling(50).max().dropna()
    resistencia_menor_5m = datos_5min["c"].rolling(50).max().dropna()
    resistencia_punto_mayor_5m = resistencia_mayor_5m.iloc[-1]
    resistencia_punto_menor_5m = resistencia_menor_5m.iloc[-1]
    # rango de resistencia a 5 minutos en las últimas 50 velas
    for data in range(50, 0):
        precio_h = datos_5min['h'].iloc[data]
        precio_o = datos_5min['o'].iloc[data]
        precio_c = datos_5min['c'].iloc[data]
        if precio_h > resistencia_punto_menor_5m > precio_c:
            if precio_c >= precio_o:
                resistencia_punto_menor_5m = precio_c
            elif precio_c < precio_o < resistencia_punto_menor_5m:
                resistencia_punto_menor_5m = precio_o
    soporte_menor_5m = datos_5min["l"].rolling(50).min().dropna()
    soporte_mayor_5m = datos_5min["c"].rolling(50).min().dropna()
    soporte_punto_menor_5m = soporte_menor_5m.iloc[-1]
    soporte_punto_mayor_5m = soporte_mayor_5m.iloc[-1]
    # rango de soporte a 5 minutos en las últimas 50 velas
    for data in range(-50, 0):
        precio_l = datos_5min['l'].iloc[data]
        precio_o = datos_5min['o'].iloc[data]
        precio_c = datos_5min['c'].iloc[data]
        if precio_l < soporte_punto_mayor_5m < precio_c:
            if precio_c <= precio_o:
                soporte_punto_mayor_5m = precio_c
            elif precio_c > precio_o > soporte_punto_mayor_5m:
                soporte_punto_mayor_5m = precio_o
    params = {"count": 500, "granularity": "S5"}  # granularity can be in seconds S5 -
    # S30, minutes M1 - M30, hours H1 - H12, days D, weeks W or months M
    client = oandapyV20.API(access_token="e51f5c80499fd16ae7e9ff6676b3c53f-3ac97247f6df3ad7b2b3731a4b1c2dc3",
                            environment="practice")
    account_id = "101-011-12930479-001"
    candles = instruments.InstrumentsCandles(instrument=divisa, params=params)
    client.request(candles)
    ohlc_dict = candles.response["candles"]
    ohlc = pd.DataFrame(ohlc_dict)
    datos_5s = ohlc.mid.dropna().apply(pd.Series)
    datos_5s["volume"] = ohlc["volume"]
    datos_5s.index = ohlc["time"]
    datos_5s = datos_5s.apply(pd.to_numeric)
    live_data = []  # precios que recorre el par de divisa en el timeframe seleccionado
    live_price_request = pricing.PricingInfo(accountID=account_id, params={"instruments": divisa})
    rango_precios = []
    while time.time() <= timeout:
        try:
            if numero_noticias == 1:
                if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[0]:
                    time.sleep(3600)
            elif numero_noticias == 2:
                if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[0]:
                    time.sleep(3600)
                elif time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[1]:
                    time.sleep(3600)
            elif numero_noticias == 3:
                if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[0]:
                    time.sleep(3600)
                elif time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[1]:
                    time.sleep(3600)
                elif time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3] == horas_noticias[2]:
                    time.sleep(3600)
            if (f"{(int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[14:16]) - 1):02}" != \
                datos_1min.iloc[-1].name[14:16]) and \
                    (f"{(int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[14:16])):02}" != \
                     datos_1min.iloc[-1].name[14:16]):
                datos_1min = pd.read_csv("datos_M1.csv", index_col="time")
                resistencia_mayor_1m = datos_1min["h"].rolling(150).max().dropna()
                resistencia_menor_1m = datos_1min["c"].rolling(150).max().dropna()
                resistencia_punto_mayor_1m = resistencia_mayor_1m.iloc[-1]
                resistencia_punto_menor_1m = resistencia_menor_1m.iloc[-1]
                for data in range(-150, 0):
                    precio_h = datos_1min['h'].iloc[data]
                    precio_o = datos_1min['o'].iloc[data]
                    precio_c = datos_1min['c'].iloc[data]
                    if precio_h > resistencia_punto_menor_1m > precio_c:
                        if precio_c >= precio_o:
                            resistencia_punto_menor_1m = precio_c
                        elif precio_c < precio_o < resistencia_punto_menor_1m:
                            resistencia_punto_menor_1m = precio_o
                soporte_menor_1m = datos_1min["l"].rolling(150).min().dropna()
                soporte_mayor_1m = datos_1min["c"].rolling(150).min().dropna()
                soporte_punto_menor_1m = soporte_menor_1m.iloc[-1]
                soporte_punto_mayor_1m = soporte_mayor_1m.iloc[-1]
                for data in range(-50, 0):
                    precio_l = datos_1min['l'].iloc[data]
                    precio_o = datos_1min['o'].iloc[data]
                    precio_c = datos_1min['c'].iloc[data]
                    if precio_l < soporte_punto_mayor_1m < precio_c:
                        if precio_c <= precio_o:
                            soporte_punto_mayor_1m = precio_c
                        elif precio_c > precio_o > soporte_punto_mayor_1m:
                            soporte_punto_mayor_1m = precio_o
            if ((int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[15:16])) == 1 or (
                    int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[15:16])) == 6) and \
                    (datos_5min.iloc[-1].name[
                     14:16] != f"{int(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[14:16]) - 1:02}"):
                datos_5min = pd.read_csv("datos_M5.csv", index_col="time")
                resistencia_mayor_5m = datos_5min["h"].rolling(50).max().dropna()
                resistencia_menor_5m = datos_5min["c"].rolling(50).max().dropna()
                resistencia_punto_mayor_5m = resistencia_mayor_5m.iloc[-1]
                resistencia_punto_menor_5m = resistencia_menor_5m.iloc[-1]
                # rango de resistencia a 5 minutos en las últimas 50 velas
                for data in range(50, 0):
                    precio_h = datos_5min['h'].iloc[data]
                    precio_o = datos_5min['o'].iloc[data]
                    precio_c = datos_5min['c'].iloc[data]
                    if precio_h > resistencia_punto_menor_5m > precio_c:
                        if precio_c >= precio_o:
                            resistencia_punto_menor_5m = precio_c
                        elif precio_c < precio_o < resistencia_punto_menor_5m:
                            resistencia_punto_menor_5m = precio_o
                soporte_menor_5m = datos_5min["l"].rolling(50).min().dropna()
                soporte_mayor_5m = datos_5min["c"].rolling(50).min().dropna()
                soporte_punto_menor_5m = soporte_menor_5m.iloc[-1]
                soporte_punto_mayor_5m = soporte_mayor_5m.iloc[-1]
                # rango de soporte a 5 minutos en las últimas 50 velas
                for data in range(-50, 0):
                    precio_l = datos_5min['l'].iloc[data]
                    precio_o = datos_5min['o'].iloc[data]
                    precio_c = datos_5min['c'].iloc[data]
                    if precio_l < soporte_punto_mayor_5m < precio_c:
                        if precio_c <= precio_o:
                            soporte_punto_mayor_5m = precio_c
                        elif precio_c > precio_o > soporte_punto_mayor_5m:
                            soporte_punto_mayor_5m = precio_o
            starttime = time.time()
            timeout2 = starttime + 5
            while starttime <= timeout2:  # Se cuenta 5 segundos de extraccion de datos para luego filtrar
                live_price_data = client.request(live_price_request)
                live_data.append(live_price_data)
                starttime = time.time()
            for i in range(len(live_data) - 1):  # Se saca la media entre el Bid y el ask para tener el precio real
                precio = (float(live_data[i]["prices"][0]["closeoutBid"])
                          + float(live_data[i]["prices"][0]["closeoutAsk"])) / 2
                rango_precios.append(precio)
            last_data_row = pd.DataFrame(index=[live_data[-1]["time"]], columns=["o", "h", "l", "c"])
            last_data_row['o'] = round(rango_precios[0], 6)
            last_data_row['h'] = round(max(rango_precios), 6)
            last_data_row['l'] = round(min(rango_precios), 6)
            last_data_row['c'] = round(rango_precios[-1], 6)
            datos_5s = datos_5s.append(last_data_row, sort=False)
            datos_5s = datos_5s.iloc[-500:]
            datos_5s.index.name = "time"
            pd.DataFrame.to_csv(datos_5s, "datos_5s.csv")
        except:
            print("hubo error, verificar si la ejecucion continua")
        if estrategia == 1:
            signal = analisis_y_estrategia1(datos_1min, datos_5s, resistencia_punto_mayor_1m,
                                            resistencia_punto_menor_1m,
                                            soporte_punto_menor_1m, soporte_punto_mayor_1m, resistencia_punto_mayor_5m,
                                            resistencia_punto_menor_5m, soporte_punto_menor_5m, soporte_punto_mayor_5m)
        elif estrategia == 2:
            signal = analisis_y_estrategia2(datos_5s, datos_1min, divisa, resistencia_punto_mayor_1m,
                                            resistencia_punto_menor_1m, resistencia_punto_mayor_5m,
                                            resistencia_punto_menor_5m, soporte_punto_menor_1m, soporte_punto_mayor_1m,
                                            soporte_punto_menor_5m, soporte_punto_mayor_5m)
        elif estrategia == 3:
            signal = analisis_y_estrategia3(datos_5s, datos_1min, datos_5min, resistencia_punto_mayor_1m,
                                            resistencia_punto_menor_1m, resistencia_punto_mayor_5m,
                                            resistencia_punto_menor_5m, soporte_punto_menor_1m, soporte_punto_mayor_1m,
                                            soporte_punto_menor_5m, soporte_punto_mayor_5m)
        ejecucion(signal, divisa)
        live_data.clear()
        rango_precios.clear()


if __name__ == "__main__":
    primera_divisa = input("introduzca la primera divisa: ")
    segunda_divisa = input("introduzca la segunda divisa: ")
    estrategia = int(input("estrategia numero 1, 2 o 3?: "))
    mes = input("introduzca el mes de inicio: ")
    dia = input("introduzca el dia de inicio: ")
    hora = input("introduzca la hora de inicio (militar): ")
    minuto = input("introduzca el minuto de inicio: ")
    tiempo = int(input("introduzca el tiempo de ejecucion en minutos: "))
    numero_noticias = int(input("Introduzca el numero de noticias: "))
    noticia1 = 0
    noticia2 = 0
    noticia3 = 0
    if numero_noticias == 0:
        pass
    elif numero_noticias == 1:
        hora_noticia = input("Introduzca la hora de la noticia 30 minutos antes")
        minuto_noticia = input("Introduzca el minuto de la noticia 30 minutos antes")
        noticia1 = f'2020-{mes}-{dia} {hora_noticia}:{minuto_noticia}'
    elif numero_noticias == 2:
        hora_noticia1 = input("Introduzca la hora de la primera noticia 30 minutos antes")
        minuto_noticia1 = input("Introduzca el minuto de la primera noticia 30 minutos antes")
        noticia1 = f'2020-{mes}-{dia} {hora_noticia1}:{minuto_noticia1}'
        hora_noticia2 = input("Introduzca la hora de la segunda noticia 30 minutos antes")
        minuto_noticia2 = input("Introduzca el minuto de la segunda noticia 30 minutos antes")
        noticia2 = f'2020-{mes}-{dia} {hora_noticia2}:{minuto_noticia2}'
    elif numero_noticias == 3:
        hora_noticia1 = input("Introduzca la hora de la primera noticia 30 minutos antes")
        minuto_noticia1 = input("Introduzca el minuto de la noticia 30 minutos antes")
        noticia1 = f'2020-{mes}-{dia} {hora_noticia1}:{minuto_noticia1}'
        hora_noticia2 = input("Introduzca la hora de la segunda noticia 30 minutos antes")
        minuto_noticia2 = input("Introduzca el minuto de la segunda noticia 30 minutos antes")
        noticia2 = f'2020-{mes}-{dia} {hora_noticia2}:{minuto_noticia2}'
        hora_noticia3 = input("Introduzca la hora de la tercera noticia 30 minutos antes")
        minuto_noticia3 = input("Introduzca el minuto de la tercera noticia 30 minutos antes")
        noticia3 = f'2020-{mes}-{dia} {hora_noticia1}:{minuto_noticia1}'
    while time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) != f'2020-{mes}-{dia} {hora}:{minuto}:00':
        pass
    run(tiempo, primera_divisa, segunda_divisa, estrategia, numero_noticias, (noticia1, noticia2, noticia3))
