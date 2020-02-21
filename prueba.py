import pandas as pd
import cv2
import time
from imagesearch import imagesearch, imagesearcharea
from analisis_y_estrategia import engulfing
import pyautogui
import random
import psutil
from multiprocessing import Process
from ExtraccionDatos10s import extraccion_10s_continua
import os

def r(num, rand):
    return num + rand * random.random()


def click_image(image, pos, action, timestamp, offset=5):
    img = cv2.imread(image)
    height, width, channels = img.shape
    pyautogui.moveTo(pos[0] + r(width / 2, offset), pos[1] + r(height / 2, offset),
                     timestamp)
    pyautogui.click(button=action)


def proceso():
    proceso_10s = Process(target=extraccion_10s_continua, name="extraccion", args=("EUR_USD",))
    proceso_10s.start()
    print(os.getpid())


if __name__ == "__main__":
    click_image("par.jpg", (489, 228), "left", 0.05)
    time.sleep(0.3)
    pyautogui.leftClick(x=1072, y=290)
    pyautogui.leftClick(x=1072, y=290)
    pyautogui.leftClick(x=1072, y=290)
    pyautogui.leftClick(x=1072, y=290)
    pyautogui.leftClick(x=1072, y=290)
    pyautogui.leftClick(x=1072, y=290)
    pyautogui.leftClick(x=1072, y=290)
    pyautogui.leftClick(x=1072, y=290)
    click_image("par_eur_usd.jpg", (817, 475), "left", 0.05)