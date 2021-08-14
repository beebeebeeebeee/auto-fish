import pickle
import os
import itertools 
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
# Target rod index (start at index 0)
rod = int(os.getenv('rod'))-1
user_name = os.getenv('user_name')
user_input = True if os.getenv('user_input') == "True" else False
auto_fish = True if os.getenv('auto_fish') == "True" else False
monitor_index = int(os.getenv('monitor_index'))
tesseract_read = True if os.getenv('tesseract_read') == "True" else False

###########
# default val
###########
half = 1
crop_factor = 1
csv_start_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
start_time = time.time()
colors = [(228, 224, 197), (163, 228, 103), (89, 198, 217), (231, 147, 232)]
fish_color_current = [0, 0, 0, 0, 0]


def get_mouse():
    x, y = mouse.position
    return (round(x), round(y))


print("正在使用:{}\n魚竿:第{}支\n重新設定:{}".format(user_name, rod+1, user_input))

if user_input:
    input("指住左上角按Enter...")
    (screenX, screenY) = get_mouse()
    input("指住右下角按Enter...")
    (screenX2, screenY2) = get_mouse()
    input("指住感嘆號按Enter...")
    (targetX, targetY) = get_mouse()
    dict = {'screenX': screenX, 'screenY': screenY, 'screenX2': screenX2, 'screenY2': screenY2,
            'targetX': targetX, 'targetY': targetY}
    file = open('./data/{}_input.txt'.format(user_name), 'wb')
    pickle.dump(dict, file)
    file.close()
else:
    file = open('./data/{}_input.txt'.format(user_name), 'rb')
    dict = pickle.load(file)
    screenX = dict['screenX']
    screenY = dict['screenY']
    screenX2 = dict['screenX2']
    screenY2 = dict['screenY2']
    targetX = dict['targetX']
    targetY = dict['targetY']
    file.close()


screen = [[screenX, screenY], [screenX2, screenY2]]
# 驚嘆號位置
target = [targetX, targetY]
###########
# Static Fix Value
###########
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
    "bag": [(screen[1][0]-screen[0][0])*0.9457167091+screen[0][0],
            (screen[1][1]-screen[0][1])*0.5060422961+screen[0][1]],
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

cmd = [(screen[1][0]-screen[0][0])*0.5+screen[0][0],
       (screen[1][1]-screen[0][1])*1.1+screen[0][1]]

fish_name = ((screen[1][0]-screen[0][0])*0.6580706781+screen[0][0],
             (screen[1][1]-screen[0][1])*0.08117443869 +
             screen[0][1], (screen[1][0]-screen[0][0]) *
             0.953199618+screen[0][0],
             (screen[1][1]-screen[0][1])*0.1537132988+screen[0][1])
fish_price = ((screen[1][0]-screen[0][0])*0.7029608405+screen[0][0],
              (screen[1][1]-screen[0][1])*0.4421416235 +
              screen[0][1], (screen[1][0]-screen[0][0]) *
              0.923591213+screen[0][0],
              (screen[1][1]-screen[0][1])*0.5215889465+screen[0][1])
fish_color = [(screen[1][0]-screen[0][0])*0.7713097713+screen[0][0],
              (screen[1][1]-screen[0][1])*0.2904411765+screen[0][1]]

with mss() as sct:
    sct_img = sct.grab(sct.monitors[1])
    if(sct_img.width > pyautogui.size().width):
        crop_factor = sct_img.width/pyautogui.size().width


###########
# Function
###########
progress_time = 0
count = 0
repair = 0
success = 0
failed = 0
isContinueFailed = False
countinueFailedCount = 0
status = ""
interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def parse_time(ss):
    if ss < 60:
        return "{}秒".format(round(ss, 2))
    elif ss < 60 * 60:
        return "{}分".format(round(ss/60, 2))
    else:
        return "{}小時".format(round(ss/60/60, 2))


def update_status():
    global progress_time, count, repair, success, failed, status
    successRate = 0 if count == 0 else str(round((success/count *100),2))
    progress_time = parse_time(time.time() - start_time)
    print("===================================\n報告: {}\n總計: {} | 修復: {} | 總計/修復率: {}\n成功: {} | 失敗: {} | 成功率: {}%\n{}\n白: {} | 綠: {} | 藍: {} | 紫: {} | 其他: {}\n===================================".format(
        progress_time, count, repair, round(count/(repair+1)), success, failed, successRate, status, fish_color_current[0], fish_color_current[1], fish_color_current[2], fish_color_current[3], fish_color_current[4]))


def add_csv(list_of_elem,  user_name=user_name):
    # Open file in append mode
    with open("./data/{}.csv".format(user_name), 'a+', newline='', encoding='utf-8-sig') as write_obj:
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
        # img.show()
        return img.load()[x, y]


def getImageText(arr, arr2, this_time):
    global tesseract_read, status, count
    if tesseract_read:
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
            # img.save("./images/name/{}_{}.jpg".format(start_time, count))
            # img2.save("./images/price/{}_{}.jpg".format(start_time, count))
            name = pytesseract.image_to_string(img, lang='chi_tra').replace(
                '\n', '').replace(' ', '').strip().strip()
            price = pytesseract.image_to_string(img2, lang='digits').replace(
                '\n', '').replace(' ', '').strip().strip()
            add_csv(["true", name, price, this_time, csv_start_time])
            status = ("釣到! %s秒\n名稱: {}\n價錢: {}".format(name, price) %
                      (this_time))
        update_status()
    else:
        add_csv(["true", "", "", this_time, csv_start_time])
        status = ("釣到! %s秒" %
                  (this_time))
        update_status()


def move(val):
    # enable_screen()
    x, y = val
    pyautogui.moveTo(x, y)


def fishing():
    # fish button
    move(fish)
    pyautogui.click()
    # ready position
    move(get)
    status = "開始釣魚"
    update_status()


def main():
    global count, repair, success, failed, isContinueFailed, countinueFailedCount, status, fish_color_current, interrupted

    # do fish
    for _ in itertools.count(): 
        if interrupted:
            print("已停止")
            break
        time.sleep(0.1)
        fishing()

        # check the rod failed
        time.sleep(3)
        if getColor(fix["bag"][0], fix["bag"][1]) == (227, 64, 65):
            if isContinueFailed:
                countinueFailedCount += 1
                if countinueFailedCount >= 5:
                    status = "沒有錢了"
                    update_status()
                    break
            isContinueFailed = True
            status = "釣竿失敗"
            repair = repair + 1
            update_status()

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
                time.sleep(2.5-x)
            continue

        ok_to_fish = False
        isContinueFailed = False
        countinueFailedCount = 0
        # auto fish or pick fish
        if not auto_fish:
            status = "等待中"
            update_status()
            move(cmd)
            pyautogui.click()
            if input("啱用嗎?啱用打1,唔啱用按Enter") == "1":
                ok_to_fish = True
        if ok_to_fish or auto_fish:
            # checking
            isContinueFailed = False
            status = "驗查中"
            update_status()
            start_time = time.time()
            for _ in itertools.count(): 
                if(time.time()-start_time > 60):
                    status = (
                        "超過60秒沒有動作!重新開始")
                    update_status()
                    if getColor(keep[0], keep[1]) == (65, 197, 243) or getColor(keep[0], keep[1]) == (255, 199, 29):
                        move(keep)
                        pyautogui.click()
                        time.sleep(0.5)
                    break
                if getColor(target[0], target[1]) == (255, 255, 255):
                    status = ("有感嘆號,釣緊")
                    update_status()
                    move(get)
                    pyautogui.click()
                    while True:
                        if getColor(keep[0], keep[1]) == (65, 197, 243) or getColor(keep[0], keep[1]) == (255, 199, 29):
                            count += 1
                            success += 1
                            color_index = 4
                            try:
                                color_index = colors.index(
                                    getColor(fish_color[0], fish_color[1]))
                            except:
                                pass
                            fish_color_current[color_index] += 1
                            update_status()
                            this_time = round(time.time() - start_time, 2)
                            # get the image (name)
                            getImageText(fish_name, fish_price, this_time)
                            # wait for keep button
                            move(keep)
                            pyautogui.click()
                            time.sleep(0.5)
                            break
                        # 斷線
                        elif getColor(fix["bag"][0], fix["bag"][1]) == (227, 64, 65):
                            count = count+1
                            failed = failed + 1
                            this_time = round(time.time() - start_time, 2)
                            status = ("失敗! %s秒" %
                                      (this_time))
                            update_status()
                            add_csv(
                                ["false", "", "", this_time, csv_start_time])
                            break
                    break
        else:
            status = ("唔啱用!")
            update_status()
            move(get)
            pyautogui.click()
            time.sleep(1)


input("按Enter開始")
main()
