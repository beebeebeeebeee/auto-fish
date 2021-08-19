from pynput.mouse import Controller
from dotenv import load_dotenv
from pathlib import Path
from pyautogui import *
from PIL import Image
from mss import mss
import itertools
import pyautogui
import pickle
import time
import os

load_dotenv(dotenv_path=Path('./.env'))
pyautogui.PAUSE = 0
mouse = Controller()


class Play():
    start_time = None

    def __init__(self):
        self.start_time = time.time()

        self.user_input = True if os.getenv('user_input') == "True" else False
        self.auto_fish = True if os.getenv('auto_fish') == "True" else False
        self.monitor_index = int(os.getenv('monitor_index'))
        self.user_name = os.getenv('user_name')
        self.rod = int(os.getenv('rod'))-1

        self.crop_factor = 1
        self.colors = [(228, 224, 197), (163, 228, 103),
                       (89, 198, 217), (231, 147, 232)]
        self.fish_color_current = [0, 0, 0, 0, 0]

        self.progress_time = 0
        self.count = 0
        self.repair = 0
        self.success = 0
        self.failed = 0
        self.is_continue_failed = False
        self.continue_failed_count = 0
        self.is_continue_failed_fishing = False
        self.continue_failed_count_fishing = 0
        self.status = ""

    def get_mouse(self):
        x, y = mouse.position
        return (round(x), round(y))

    def move(self, val):
        x, y = val
        pyautogui.moveTo(x, y)

    def click(self):
        pyautogui.click()

    def parse_time(self, time):
        if time < 60:
            return "{}秒".format(round(time, 2))
        elif time < 60 * 60:
            return "{}分".format(round(time/60, 2))
        else:
            return "{}小時".format(round(time/60/60, 2))

    def ask_settings(self, props):
        if(props == None):
            print("正在使用:{}\n魚竿:第{}支\n重新設定:{}".format(
                self.user_name, self.rod+1, self.user_input))
            if self.user_input:
                input("指住左上角按Enter...")
                (self.screenX, self.screenY) = self.get_mouse()
                input("指住右下角按Enter...")
                (self.screenX2, self.screenY2) = self.get_mouse()
                input("指住感嘆號按Enter...")
                (self.targetX, self.targetY) = self.get_mouse()
                self.dict = {'screenX': self.screenX, 'screenY': self.screenY, 'screenX2': self.screenX2, 'screenY2': self.screenY2,
                            'targetX': self.targetX, 'targetY': self.targetY}
                file = open('./data/{}_input.txt'.format(self.user_name), 'wb')
                pickle.dump(self.dict, file)
                file.close()
            else:
                file = open('./data/{}_input.txt'.format(self.user_name), 'rb')
                dict = pickle.load(file)
                self.screenX = dict['screenX']
                self.screenY = dict['screenY']
                self.screenX2 = dict['screenX2']
                self.screenY2 = dict['screenY2']
                self.targetX = dict['targetX']
                self.targetY = dict['targetY']
                file.close()
            self.screen = [[self.screenX, self.screenY],
                        [self.screenX2, self.screenY2]]
            # 驚嘆號位置
            self.target = [self.targetX, self.targetY]
        else:
            self.rod = props['rod']-1
            self.screen = [props['screen1'],props['screen2']]
            self.target = props['target']

    def main(self, props = None):
        self.ask_settings(props)
        
        # Static Fix Value
        self.fish = [(self.screen[1][0]-self.screen[0][0])*0.8037848606+self.screen[0][0],
                     (self.screen[1][1]-self.screen[0][1])*0.6292947559+self.screen[0][1]]
        # 收釣竿
        self.get = [(self.screen[1][0]-self.screen[0][0])*0.88944223107+self.screen[0][0],
                    (self.screen[1][1]-self.screen[0][1])*0.77938517179+self.screen[0][1]]
        # 保管
        self.keep = [(self.screen[1][0]-self.screen[0][0])*0.76195219123+self.screen[0][0],
                     (self.screen[1][1]-self.screen[0][1])*0.80831826401+self.screen[0][1]]

        self.fix = {
            "bag": [(self.screen[1][0]-self.screen[0][0])*0.9457167091+self.screen[0][0],
                    (self.screen[1][1]-self.screen[0][1])*0.5060422961+self.screen[0][1]],
            "menu": [(self.screen[1][0]-self.screen[0][0])*0.7239304813+self.screen[0][0],
                     (self.screen[1][1]-self.screen[0][1])*0.06904761905+self.screen[0][1]],
            "fix": [[(self.screen[1][0]-self.screen[0][0])*0.6102941176+self.screen[0][0],
                     (self.screen[1][1]-self.screen[0][1])*0.4797619048+self.screen[0][1]], [(self.screen[1][0]-self.screen[0][0])*0.7640374332+self.screen[0][0],
                                                                                             (self.screen[1][1]-self.screen[0][1])*0.4797619048+self.screen[0][1]], [(self.screen[1][0]-self.screen[0][0])*0.9177807487+self.screen[0][0],
                                                                                                                                                                     (self.screen[1][1]-self.screen[0][1])*0.4797619048+self.screen[0][1]], [(self.screen[1][0]-self.screen[0][0])*0.6102941176+self.screen[0][0],
                                                                                                                                                                                                                                             (self.screen[1][1]-self.screen[0][1])*0.830952381+self.screen[0][1]], [(self.screen[1][0]-self.screen[0][0])*0.7640374332+self.screen[0][0],
                                                                                                                                                                                                                                                                                                                    (self.screen[1][1]-self.screen[0][1])*0.830952381+self.screen[0][1]], [(self.screen[1][0]-self.screen[0][0])*0.9177807487+self.screen[0][0],
                                                                                                                                                                                                                                                                                                                                                                                           (self.screen[1][1]-self.screen[0][1])*0.830952381+self.screen[0][1]]],
            "paid": [(self.screen[1][0]-self.screen[0][0])*0.5060160428+self.screen[0][0],
                     (self.screen[1][1]-self.screen[0][1])*0.7607142857+self.screen[0][1]]
        }

        self.cmd = [(self.screen[1][0]-self.screen[0][0])*0.5+self.screen[0][0],
                    (self.screen[1][1]-self.screen[0][1])*1.1+self.screen[0][1]]

        self.fish_name = ((self.screen[1][0]-self.screen[0][0])*0.6580706781+self.screen[0][0],
                          (self.screen[1][1]-self.screen[0][1])*0.08117443869 +
                          self.screen[0][1], (self.screen[1][0]-self.screen[0][0]) *
                          0.953199618+self.screen[0][0],
                          (self.screen[1][1]-self.screen[0][1])*0.1537132988+self.screen[0][1])
        self.fish_price = ((self.screen[1][0]-self.screen[0][0])*0.7029608405+self.screen[0][0],
                           (self.screen[1][1]-self.screen[0][1])*0.4421416235 +
                           self.screen[0][1], (self.screen[1][0]-self.screen[0][0]) *
                           0.923591213+self.screen[0][0],
                           (self.screen[1][1]-self.screen[0][1])*0.5215889465+self.screen[0][1])
        self.fish_color = [(self.screen[1][0]-self.screen[0][0])*0.7713097713+self.screen[0][0],
                           (self.screen[1][1]-self.screen[0][1])*0.2904411765+self.screen[0][1]]

        with mss() as sct:
            sct_img = sct.grab(sct.monitors[1])
            if(sct_img.width > pyautogui.size().width):
                self.crop_factor = sct_img.width/pyautogui.size().width
        if __name__ == "__main__":
            input("按Enter開始")
        self.start()

    def update_status(self):
        success_rate = 0 if self.count == 0 else str(
            round((self.success/self.count * 100), 2))
        progress_time = self.parse_time(time.time() - self.start_time)
        print("===================================\n報告: {}\n總計: {} | 修復: {} | 總計/修復率: {}\n成功: {} | 失敗: {} | 成功率: {}%\n{}\n白: {} | 綠: {} | 藍: {} | 紫: {} | 其他: {}\n===================================".format(
            progress_time, self.count, self.repair, round(self.count/(self.repair+1)), self.success, self.failed, success_rate, self.status, self.fish_color_current[0], self.fish_color_current[1], self.fish_color_current[2], self.fish_color_current[3], self.fish_color_current[4]))

    def getColor(self, x, y):
        with mss() as sct:
            sct_img = sct.grab(sct.monitors[self.monitor_index])
            x = x*self.crop_factor
            y = y*self.crop_factor
            img = Image.frombytes("RGB", sct_img.size,
                                  sct_img.bgra, "raw", "BGRX")
            return img.load()[x, y]

    def fishing(self):
        self.move(self.fish)
        self.click()
        self.status = "開始釣魚"
        self.update_status()

    def start(self):
        # do fish
        for _ in itertools.count():
            time.sleep(0.1)
            self.fishing()

            # check the rod failed
            time.sleep(3)
            if self.getColor(self.fix["bag"][0], self.fix["bag"][1]) == (227, 64, 65):
                if self.is_continue_failed:
                    self.continue_failed_count += 1
                    if self.continue_failed_count >= 5:
                        self.status = "沒有錢了，即將停止程序。"
                        self.update_status()
                        exit()
                self.is_continue_failed = True
                self.status = "釣竿失敗"
                self.repair += 1
                self.update_status()

                self.move(self.fix["bag"])
                self.click()
                time.sleep(0.5)
                self.move(self.fix["menu"])
                self.click()
                time.sleep(0.5)
                self.move(self.fix["fix"][self.rod])
                self.click()
                time.sleep(0.5)
                for x in range(3):
                    self.move(self.fix["paid"])
                    self.click()
                    time.sleep(2.5-x)
                continue

            ok_to_fish = False
            self.is_continue_failed = False
            self.continue_failed_count = 0
            # auto fish or pick fish
            if not self.auto_fish:
                self.status = "等待中"
                self.update_status()
                self.move(self.cmd)
                self.click()
                if input("啱用嗎?啱用打1,唔啱用按Enter") == "1":
                    ok_to_fish = True
            if ok_to_fish or self.auto_fish:
                # checking
                self.is_continue_failed = False
                self.status = "驗查中"
                self.update_status()
                fishing_time = time.time()
                for _ in itertools.count():
                    if(time.time()-fishing_time > 60):
                        if self.continue_failed_count_fishing >= 4:
                            self.status = "有嚴重問題，即將停止程序。"
                            self.update_status()
                            exit()
                        else:
                            self.continue_failed_count_fishing += 1
                            self.status = (
                                "超過60秒沒有動作!重新開始")
                            self.update_status()
                            if self.getColor(self.keep[0], self.keep[1]) == (65, 197, 243) or self.getColor(self.keep[0], self.keep[1]) == (255, 199, 29):
                                self.move(self.keep)
                                self.click()
                                time.sleep(0.5)
                            break
                    if self.getColor(self.target[0], self.target[1]) == (255, 255, 255):
                        self.continue_failed_count_fishing = 0
                        self.status = ("有感嘆號,釣緊")
                        self.update_status()
                        self.move(self.get)
                        self.click()
                        start_fishing_time = time.time()
                        for _ in itertools.count():
                            if self.getColor(self.keep[0], self.keep[1]) == (65, 197, 243) or self.getColor(self.keep[0], self.keep[1]) == (255, 199, 29):
                                self.count += 1
                                self.success += 1
                                color_index = 4
                                try:
                                    color_index = self.colors.index(
                                        self.getColor(self.fish_color[0], self.fish_color[1]))
                                except:
                                    pass
                                self.fish_color_current[color_index] += 1
                                self.update_status()
                                this_time = round(time.time() - fishing_time, 2)
                                # get the image (name)
                                self.status = ("釣到! %s秒" % (this_time))
                                self.update_status()
                                # wait for keep button
                                self.move(self.keep)
                                self.click()
                                time.sleep(0.5)
                                break
                            # 斷線
                            elif self.getColor(self.fix["bag"][0], self.fix["bag"][1]) == (227, 64, 65):
                                self.count += 1
                                self.failed += 1
                                this_time = round(time.time() - self.start_time, 2)
                                self.status = ("失敗! %s秒" %
                                          (this_time))
                                self.update_status()
                                break
                            elif time.time() - start_fishing_time > 60:
                                self.status = ("超過60秒沒有動作!有嚴重問題，即將停止程序。")
                                self.update_status()
                                exit()
                        break
            else:
                self.status = ("唔啱用!")
                self.update_status()
                self.move(self.get)
                self.click()
                time.sleep(1)


if __name__ == "__main__":
    Play().main()
