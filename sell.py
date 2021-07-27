import pickle
import os
from dotenv import load_dotenv
from pyautogui import *
import pyautogui
import time
from datetime import datetime
from PIL import Image
from mss import mss
from csv import writer
from pathlib import Path
import numpy
import cv2 as cv
import pytesseract
from pynput.mouse import Button, Controller

mouse = Controller()
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pyautogui.PAUSE = 0
load_dotenv(dotenv_path=Path('./.env'))

###########
# env val
###########
monitor_index = int(os.getenv('monitor_index'))
sell_option = int(os.getenv('sell_option'))
user_name = os.getenv('user_name')
user_input = True if os.getenv('user_input') == "True" else False

half = 1
crop_factor = 1
csv_start_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
start_time = time.time()

sell_color = [[(228, 224, 197)], [(228, 224, 197), (163, 228, 103)], [
    (228, 224, 197), (163, 228, 103), (89, 198, 217)]]


def get_mouse():
    x, y = mouse.position
    return (round(x), round(y))


with mss() as sct:
    sct_img = sct.grab(sct.monitors[1])
    if(sct_img.width > pyautogui.size().width):
        crop_factor = sct_img.width/pyautogui.size().width


def getColor(x, y):
    with mss() as sct:
        sct_img = sct.grab(sct.monitors[monitor_index])
        x = x*crop_factor
        y = y*crop_factor
        # Convert to PIL.Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        # img.show()
        return img.load()[x, y]


def click(val):
    # enable_screen()
    x, y = val
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(0.2)


if user_input:
    input("指住左上角按Enter...")
    (screenX, screenY) = get_mouse()
    input("指住右下角按Enter...")
    (screenX2, screenY2) = get_mouse()
else:
    file = open('./data/{}_input.txt'.format(user_name), 'rb')
    dict = pickle.load(file)
    screenX = dict['screenX']
    screenY = dict['screenY']
    screenX2 = dict['screenX2']
    screenY2 = dict['screenY2']
    file.close()

screen = [[screenX, screenY], [screenX2, screenY2]]

radioX = [0.5100105374, 0.6438356164, 0.7650158061, 0.9051633298]
radioY = [0.1925233645, 0.4642056075, 0.7327102804]
table = []
sort = [(screen[1][0]-screen[0][0])*0.9726027397+screen[0][0],
        (screen[1][1]-screen[0][1])*0.9663551402+screen[0][1]]
sell1 = [(screen[1][0]-screen[0][0])*0.6733403583+screen[0][0],
         (screen[1][1]-screen[0][1])*0.9345794393+screen[0][1]]
sell2 = [(screen[1][0]-screen[0][0])*0.4457323498+screen[0][0],
         (screen[1][1]-screen[0][1])*0.7551401869+screen[0][1]]
for y in radioY:
    for x in radioX:
        table.append([(screen[1][0]-screen[0][0])*x+screen[0][0],
                      (screen[1][1]-screen[0][1])*y+screen[0][1]])

have_color = False
first_time = True
times = 0.5
input("按Enter開始")
print("%s秒後開始" % times)
time.sleep(times)
while not have_color:
    tem1 = getColor(table[0][0], table[0][1])
    tem2 = getColor(table[3][0], table[3][1])
    tem3 = getColor(table[8][0], table[8][1])
    tem4 = getColor(table[11][0], table[11][1])
    print("驗查更新排序 (第一次)")
    click(sort)
    for i in range(100000):
        if getColor(table[0][0], table[0][1]) != tem1 or getColor(table[3][0], table[3][1]) != tem2 or getColor(table[8][0], table[8][1]) != tem3 or getColor(table[11][0], table[11][1]) != tem4:
            break
    if first_time:
        first_time = False
    else:
        tem1 = getColor(table[0][0], table[0][1])
        tem2 = getColor(table[3][0], table[3][1])
        tem3 = getColor(table[8][0], table[8][1])
        tem4 = getColor(table[11][0], table[11][1])
        print("驗查更新排序 (第二次)")
        click(sort)
        for i in range(100000):
            if getColor(table[0][0], table[0][1]) != tem1 or getColor(table[3][0], table[3][1]) != tem2 or getColor(table[8][0], table[8][1]) != tem3 or getColor(table[11][0], table[11][1]) != tem4:
                break
    print("驗查魚類")
    for each in table:
        if getColor(each[0], each[1]) in sell_color[sell_option]:
            click(each)
        else:
            have_color = True
            break
    print("賣魚")
    click(sell1)
    for i in range(100000):
        if getColor(sell2[0], sell2[1]) == (65, 197, 243):
            break
    print("確定賣魚")
    click(sell2)
    for i in range(100000):
        if getColor(sell2[0], sell2[1]) == (65, 197, 243):
            break
    print("完成賣魚")
    click(sell2)
