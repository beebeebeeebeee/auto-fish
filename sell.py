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

BUTTON_BLUE = (65, 197, 243)
START_WAIT_TIME = 0

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

def click_fast(val):
    # enable_screen()
    x, y = val
    pyautogui.moveTo(x, y)
    pyautogui.click()


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
         (screen[1][1]-screen[0][1])*0.7651401869+screen[0][1]]
sell3 = [(screen[1][0]-screen[0][0])*0.4457323498+screen[0][0],
         (screen[1][1]-screen[0][1])*0.7451401869+screen[0][1]]

sort_notice = [(screen[1][0]-screen[0][0])*0.8033403583+screen[0][0],
               (screen[1][1]-screen[0][1])*0.9345794393+screen[0][1]]
for y in radioY:
    for x in radioX:
        table.append([(screen[1][0]-screen[0][0])*x+screen[0][0],
                      (screen[1][1]-screen[0][1])*y+screen[0][1]])


def storeBoard():
    board = []
    for each in table:
        board.append(getColor(each[0], each[1]))
    return board


def hasChanges(b1, b2):
    for index, each in enumerate(b1):
        if each != b2[index]:
            return True
    return False

have_color = False
first_time = True
count_fish = 0
input("按Enter開始")
print("%s秒後開始" % START_WAIT_TIME)
time.sleep(START_WAIT_TIME)

while not have_color:
    print("驗查更新排序 (第一次)")
    click(sort)
    for i in range(100000):
        if not first_time:
            if getColor(sort_notice[0], sort_notice[1]) != BUTTON_BLUE:
                break
        else:
            tem1 = storeBoard()
            if hasChanges(tem1, storeBoard()):
                break
    
    if first_time:
        first_time = False
    else:
        print("驗查更新排序 (第二次)")
        click(sort)
        for i in range(100000):
            if getColor(sort_notice[0], sort_notice[1]) == BUTTON_BLUE:
                break
        for i in range(100000):
            if getColor(sort_notice[0], sort_notice[1]) != BUTTON_BLUE:
                break
    print("驗查魚類")
    this_fish = 0
    for each in table:
        if getColor(each[0], each[1]) in sell_color[sell_option]:
            click_fast(each)
            count_fish += 1
            this_fish += 1
        else:
            have_color = True
            break
    print("賣魚 {}/{}".format(this_fish, count_fish))
    click(sell1)
    for i in range(100000):
        if getColor(sell2[0], sell2[1]) == BUTTON_BLUE:
            break
    print("確定賣魚")
    click(sell2)
    for i in range(100000):
        if getColor(sell2[0], sell2[1]) != BUTTON_BLUE:
            break
    for i in range(100000):
        if getColor(sell3[0], sell3[1]) == BUTTON_BLUE:
            break
    print("完成賣魚")
    click(sell3)
