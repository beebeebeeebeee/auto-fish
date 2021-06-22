from pyautogui import *
import pyautogui
import time
from datetime import datetime
from PIL import Image
from mss import mss
from csv import writer
import numpy
import cv2 as cv
import pytesseract
from pynput.mouse import Button, Controller
mouse = Controller()

pyautogui.PAUSE = 0


###########
# Change Here
###########
# Target rod index
rod = 5
monitor_index = 1
half = 1

def get_mouse():
    x,y = mouse.position
    return (round(x),round(y))

input("Press Enter to get screen 1...")
(screenX, screenY) = get_mouse()
input("Press Enter to get screen 2...")
(screenX2, screenY2) = get_mouse()
input("Press Enter to get 驚嘆號...")
(targetX, targetY) = get_mouse()
input("Press Enter to get fail chat...")
(failX, failY) = get_mouse()

screen = [[screenX, screenY], [screenX2, screenY2]]
# 驚嘆號位置
target = [targetX, targetY]
# fail chat
fail = [failX, failY]
###########
# Static Fix Value
###########
# top bar of game
top = [(screen[1][0]-screen[0][0])/2, screen[0][1]-half]
# 開始釣魚
fish = [(screen[1][0]-screen[0][0])*0.8037848606+screen[0][0],
        (screen[1][1]-screen[0][1])*0.6292947559+screen[0][1]]
# 收釣竿
get = [(screen[1][0]-screen[0][0])*0.88944223107+screen[0][0],
       (screen[1][1]-screen[0][1])*0.77938517179+screen[0][1]]
# 保管
keep = [(screen[1][0]-screen[0][0])*0.76195219123+screen[0][0],
        (screen[1][1]-screen[0][1])*0.80831826401+screen[0][1]]

fix = {
    "bag": [(screen[1][0]-screen[0][0])*0.9612299465+screen[0][0],
            (screen[1][1]-screen[0][1])*0.5404761905+screen[0][1]],
    "menu": [(screen[1][0]-screen[0][0])*0.7239304813+screen[0][0],
             (screen[1][1]-screen[0][1])*0.06904761905+screen[0][1]],
    "fix": [[(screen[1][0]-screen[0][0])*0.6102941176+screen[0][0],
             (screen[1][1]-screen[0][1])*0.4797619048+screen[0][1]], [(screen[1][0]-screen[0][0])*0.7640374332+screen[0][0],
                                                                      (screen[1][1]-screen[0][1])*0.4797619048+screen[0][1]], [(screen[1][0]-screen[0][0])*0.9177807487+screen[0][0],
                                                                                                                               (screen[1][1]-screen[0][1])*0.4797619048+screen[0][1]], [(screen[1][0]-screen[0][0])*0.6102941176+screen[0][0],
                                                                                                                                                                                        (screen[1][1]-screen[0][1])*0.830952381+screen[0][1]], [(screen[1][0]-screen[0][0])*0.7640374332+screen[0][0],
                                                                                                                                                                                                                                                (screen[1][1]-screen[0][1])*0.830952381+screen[0][1]], [(screen[1][0]-screen[0][0])*0.9177807487+screen[0][0],
                                                                                                                                                                                                                                                                                                        (screen[1][1]-screen[0][1])*0.830952381+screen[0][1]]],
    "paid": [(screen[1][0]-screen[0][0])*0.5060160428+screen[0][0],
             (screen[1][1]-screen[0][1])*0.7607142857+screen[0][1]]
}

fish_name = ((screen[1][0]-screen[0][0])*0.6580706781+screen[0][0],
             (screen[1][1]-screen[0][1])*0.08117443869+screen[0][1],(screen[1][0]-screen[0][0])*0.953199618+screen[0][0],
             (screen[1][1]-screen[0][1])*0.1537132988+screen[0][1])
fish_price = ((screen[1][0]-screen[0][0])*0.7029608405+screen[0][0],
             (screen[1][1]-screen[0][1])*0.4421416235+screen[0][1],(screen[1][0]-screen[0][0])*0.923591213+screen[0][0],
             (screen[1][1]-screen[0][1])*0.5215889465+screen[0][1])

csv_start_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

crop_factor = 1

with mss() as sct:
    sct_img = sct.grab(sct.monitors[1])
    if(sct_img.width > pyautogui.size().width):
        crop_factor = sct_img.width/pyautogui.size().width


###########
# Function
###########

def add_csv(list_of_elem,  file_name="record.csv"):
    # Open file in append mode
    with open(file_name, 'a+', newline='', encoding='utf-8-sig') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


def getColor(x, y):
    with mss() as sct:
        sct_img = sct.grab(sct.monitors[monitor_index])
        x = x*crop_factor
        y = y*crop_factor
        # Convert to PIL.Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return img.load()[x, y]


def getImageText(arr, arr2, this_time):
    (x, y, x2, y2) = arr
    (nx, ny, nx2, ny2) = arr2
    with mss() as sct:
        sct_img = sct.grab(sct.monitors[monitor_index])
        x = x*crop_factor
        y = y*crop_factor
        x2 = x2*crop_factor
        y2 = y2*crop_factor
        nx = nx*crop_factor
        ny = ny*crop_factor
        nx2 = nx2*crop_factor
        ny2 = ny2*crop_factor
        # Convert to PIL.Image
        img = Image.frombytes("RGB", sct_img.size,
                              sct_img.bgra, "raw", "BGRX").crop((x, y, x2, y2))
        img2 = Image.frombytes("RGB", sct_img.size,
                              sct_img.bgra, "raw", "BGRX").crop((nx, ny, nx2, ny2))
        name = pytesseract.image_to_string(img, lang='chi_tra').replace('\n','').replace(' ','').strip().strip()
        price = int(pytesseract.image_to_string(img2, lang='digits').replace('\n','').replace(' ','').strip().strip())
        add_csv(["true", name, price, this_time, csv_start_time])


def move(val):
    x, y = val
    pyautogui.moveTo(x, y)


def fishing():
    # fish button
    move(fish)
    pyautogui.click()
    # ready position
    move(get)
    print("start fishing")


def main():
    count = 0

    # enable the game view
    move(top)
    pyautogui.click()

    # do fish
    for n in range(0, 100000000):
        time.sleep(0.1)
        fishing()

        # check the rod failed
        time.sleep(2)
        print(getColor(fail[0], fail[1]))
        if getColor(fail[0], fail[1]) == (255, 255, 255):
            print("rod fail")
            move(fix["bag"])
            pyautogui.click()
            time.sleep(0.5)
            move(fix["menu"])
            pyautogui.click()
            time.sleep(0.5)
            move(fix["fix"][rod])
            pyautogui.click()
            time.sleep(0.5)
            for x in range(3):
                move(fix["paid"])
                pyautogui.click()
                time.sleep(2.5)
            continue

        # checking
        print("checking")
        start_time = time.time()
        for k in range(0, 100000000):
            if getColor(target[0], target[1]) == (255, 255, 255):
                pyautogui.click()
                while True:
                    if getColor(keep[0], keep[1]) == (65, 197, 243) or getColor(keep[0], keep[1]) == (255, 199, 29):
                        count = count+1
                        this_time = round(time.time() - start_time,2)
                        # get the image (name)
                        (name, price) = getImageText(fish_name, fish_price, this_time)
                        print("Got it! {} %ss\nName: {}\nPrice: {}".format(count,name,price) %
                              (this_time))
                        # wait for keep button
                        move(keep)
                        pyautogui.click()
                        time.sleep(0.5)
                        break
                    # 斷線
                    elif getColor(fail[0], fail[1]) == (255, 255, 255):
                        this_time = round(time.time() - start_time,2)
                        print("Failed! {} %ss".format(count) %
                              (this_time))
                        add_csv(["false", "", "", this_time, csv_start_time])
                        break
                break


# exit()
input("Press Enter Start!")
main()
# print(getImageText((159, 86,404,250),True))
