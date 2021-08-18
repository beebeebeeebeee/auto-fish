from pynput.mouse import Controller
from dotenv import load_dotenv
from pathlib import Path
from pyautogui import *
# from PIL import Image
# from mss import mss
import itertools
# import pyautogui
import keyboard
import pickle
# import time
# import os
import tkinter as tk
from tkinter import ttk

import rx
from rx.scheduler import ThreadPoolScheduler

load_dotenv(dotenv_path=Path('./.env'))
# pyautogui.PAUSE = 0
mouse = Controller()

class AutoFishGUI:
    font_xs = ('Helvatical bold', 16)
    font = ('Helvatical bold', 20)
    font_lg = ('Helvatical bold', 40)

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

    def __init__(self, master):
        self.master = master
        self.pool_scheduler = ThreadPoolScheduler(1)
        master.title("Auto Fish GUI 自動魚圖形用戶界面")
        master.geometry("600x400")
        self.tabControl = ttk.Notebook(master)

        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.init_tab1(self.tab1)
        self.init_tab2(self.tab2)
        self.tabControl.add(self.tab1, text='設置')
        self.tabControl.add(self.tab2, text='狀態監視器')

        # self.profileList.insert(0, "bee", "tiffy")

    def init_tab1(self, tab):
        self.tabControl.pack(expand=1, fill="both")

        self.profileList = tk.Listbox(tab, height=14, width=15, font=self.font_xs)
        self.profileList.grid(row=0, column=0, rowspan=14, columnspan=2)
        self.profileList.bind("<<ListboxSelect>>", self.select_profile)

        tk.Label(tab, text="魚竿", font=self.font).grid(row=0, column=2)
        tk.Label(tab, text="左上角", font=self.font).grid(row=1, column=2)
        tk.Label(tab, text="右下角", font=self.font).grid(row=2, column=2)
        tk.Label(tab, text="感嘆號", font=self.font).grid(row=3, column=2)

        self.rod = tk.StringVar()
        tk.Entry(tab, textvariable=self.rod).grid(row=0, column=3)
        self.screen1 = tk.StringVar()
        tk.Entry(tab, textvariable=self.screen1).grid(row=1, column=3)
        self.screen2 = tk.StringVar()
        tk.Entry(tab, textvariable=self.screen2).grid(row=2, column=3)
        self.target = tk.StringVar()
        tk.Entry(tab, textvariable=self.target).grid(row=3, column=3)

        tk.Button(tab, text="調整位置", command=lambda: self.adjust_position(
            self.screen1)).grid(row=1, column=4)
        tk.Button(tab, text="調整位置", command=lambda: self.adjust_position(
            self.screen2)).grid(row=2, column=4)
        tk.Button(tab, text="調整位置", command=lambda: self.adjust_position(
            self.target)).grid(row=3, column=4)

        tk.Button(tab, height=1, width=14, text="開始釣魚", font=self.font,
                  command=self.start_fish).grid(row=5, column=2, columnspan=3)
        tk.Button(tab, height=1, width=14, text="Copy Profile", font=self.font,
                  command=self.copy_profile).grid(row=6, column=2, columnspan=3)

    def init_tab2(self, tab):
        pass

    def select_profile(self, event):
        selection = event.widget.get(event.widget.curselection()[0])
        print(selection)

        try:
            file = open('data.txt', 'rb')
            file.close()
        except():
            file = open('data.txt', 'wb')
            file.close()
        
        file = open('data.txt', 'rb')
        
        dict = pickle.load(file)
        self.rod.set(int(os.getenv('rod'))-1)
        self.screen1.set([dict['screenX'], dict['screenY']])
        self.screen2.set([dict['screenX2'], dict['screenY2']])
        self.target.set([dict['targetX'], dict['targetY']])
        file.close()

    def adjust_position(self, target):
        def running(_):
            self.adjust_current_stoped = False
            for _ in itertools.count():
                if keyboard.is_pressed('q'):
                    position = self.get_mouse()
                    target.set(position)
                    break
                if keyboard.is_pressed('c'):
                    target.set(self.adjust_current_prev)
                    break
                if self.adjust_current_stoped:
                    break

        def on_task_done():
            self.adjust_current = None

        if(hasattr(self, 'adjust_current') and self.adjust_current != None):
            self.adjust_current.set(self.adjust_current_prev)

        self.adjust_current_stoped = True
        self.adjust_current = target
        self.adjust_current_prev = target.get()
        target.set("按 Q 設置位置或按 C 取消")
        self.master.update()
        rx.just(1).subscribe(
            on_next=running,
            on_completed=lambda: self.master.after(5, on_task_done),
            scheduler=self.pool_scheduler
        )

    def start_fish(self):
        pass

    def copy_profile(self):
        profile_name = tk.StringVar()

        def done():
            if(x := profile_name.get()) != "":
                win.destroy()
                self.profileList.insert(0, x)

        win = tk.Toplevel()
        win.wm_title("Profile Name")
        win.wm_geometry("300x100")

        tk.Entry(win, textvariable=profile_name,
                 font=self.font).grid(row=0, column=0)

        tk.Button(win, text="Okay", command=done,
                   font=self.font).grid(row=1, column=0)


if __name__ == "__main__":
    root = tk.Tk()
    autoFishGUI = AutoFishGUI(root)
    root.mainloop()
