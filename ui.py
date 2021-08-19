from pynput.mouse import Controller
from dotenv import load_dotenv
from pathlib import Path
from pyautogui import *
from PIL import Image
from mss import mss
import itertools
import pyautogui
import keyboard
import json
import time
import os
import tkinter as tk
from tkinter import ttk

import rx
from rx.scheduler import ThreadPoolScheduler

import play

load_dotenv(dotenv_path=Path('./.env'))
# pyautogui.PAUSE = 0
mouse = Controller()


class AutoFishGUI:
    font_xs = ('Helvatical bold', 16)
    font = ('Helvatical bold', 20)
    font_lg = ('Helvatical bold', 40)
    writepath = 'data.json'

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

    def getJson(self):
        self.profileListData = []
        if os.path.exists(self.writepath):
            self.profileListData = json.load(open(self.writepath,)).keys()
        else:
            with open(self.writepath, 'w') as f:
                json.dump({}, f)

    def __init__(self, master):
        self.getJson()

        self.master = master
        self.pool_scheduler = ThreadPoolScheduler(1)
        master.title("Auto Fish GUI 自動魚圖形用戶界面")
        master.geometry("600x400")
        self.tabControl = ttk.Notebook(master)

        self.s = ttk.Style()
        self.s.configure('My.TFrame', background='#FFFFFF')

        self.tab1 = ttk.Frame(self.tabControl, style='My.TFrame')
        self.tab2 = ttk.Frame(self.tabControl, style='My.TFrame')
        self.init_tab1(self.tab1)
        self.init_tab2(self.tab2)
        self.tabControl.add(self.tab1, text='設置')
        self.tabControl.add(self.tab2, text='狀態監視器')

        for profile in self.profileListData:
            self.profileList.insert(0, profile)

    def init_tab1(self, tab):
        self.tabControl.pack(expand=1, fill="both")

        self.profileList = tk.Listbox(
            tab, height=14, width=15, font=self.font_xs, )
        self.profileList.grid(row=0, column=0, rowspan=14, columnspan=2)
        self.profileList.bind("<<ListboxSelect>>", self.select_profile)

        tk.Label(tab, text="魚竿", font=self.font_xs, justify=tk.RIGHT).grid(row=1, column=2)
        tk.Label(tab, text="左上角", font=self.font_xs, justify=tk.RIGHT).grid(row=2, column=2)
        tk.Label(tab, text="右下角", font=self.font_xs, justify=tk.RIGHT).grid(row=3, column=2)
        tk.Label(tab, text="感嘆號", font=self.font_xs, justify=tk.RIGHT).grid(row=4, column=2)

        self.current_profile_name = tk.StringVar()
        tk.Entry(tab, textvariable=self.current_profile_name,
                 state='disabled', width=35, justify=tk.LEFT).grid(row=0, column=2, columnspan=3)
        self.rod = tk.IntVar()
        e = tk.Entry(tab, textvariable=self.rod)
        e.grid(row=1, column=3)
        e.bind('<Return>', (lambda _: self.setRod()))
        self.screen1 = tk.StringVar()
        tk.Entry(tab, textvariable=self.screen1,
                 state='disabled').grid(row=2, column=3)
        self.screen2 = tk.StringVar()
        tk.Entry(tab, textvariable=self.screen2,
                 state='disabled').grid(row=3, column=3)
        self.target = tk.StringVar()
        tk.Entry(tab, textvariable=self.target,
                 state='disabled').grid(row=4, column=3)

        tk.Button(tab, text="調整位置", command=lambda: self.adjust_position(
            self.screen1, 'screen1')).grid(row=2, column=4)
        tk.Button(tab, text="調整位置", command=lambda: self.adjust_position(
            self.screen2, 'screen2')).grid(row=3, column=4)
        tk.Button(tab, text="調整位置", command=lambda: self.adjust_position(
            self.target, 'target')).grid(row=4, column=4)

        tk.Button(tab, height=1, width=22, text="開始釣魚", font=self.font,
                  command=self.start_fish).grid(row=5, column=2, columnspan=3)
        tk.Button(tab, height=1, width=22, text="Copy Profile", font=self.font,
                  command=self.copy_profile).grid(row=6, column=2, columnspan=3)

    def init_tab2(self, tab):
        pass

    def select_profile(self, event):
        if len(selected := event.widget.curselection()) > 0:
            self.current_profile_name.set(event.widget.get(selected[0]))
            print(self.current_profile_name.get())

            file = open(self.writepath,)
            dict = json.load(file)[self.current_profile_name.get()]
            self.rod.set(dict['rod'])
            self.screen1.set(dict['screen1'])
            self.screen2.set(dict['screen2'])
            self.target.set(dict['target'])
            file.close()

    def setRod(self):
        with open(self.writepath, "r") as f:
            d = json.load(f)
            d[self.current_profile_name.get()]['rod'] = self.rod.get()
            with open(self.writepath, "w") as f:
                json.dump(d, f)

    def adjust_position(self, target, target_name):
        def running(_):
            self.adjust_current_stopped = False
            for _ in itertools.count():
                if keyboard.is_pressed('q'):
                    target.set((t := self.get_mouse()))
                    with open(self.writepath, "r") as f:
                        d = json.load(f)
                    d[self.current_profile_name.get()][target_name] = t
                    with open(self.writepath, "w") as f:
                        json.dump(d, f)
                    break
                if keyboard.is_pressed('c'):
                    target.set(self.adjust_current_prev)
                    break
                if self.adjust_current_stopped:
                    break

        def on_task_done():
            self.adjust_current = None

        if(hasattr(self, 'adjust_current') and self.adjust_current != None):
            self.adjust_current.set(self.adjust_current_prev)

        self.adjust_current_stopped = True
        self.adjust_current = target
        self.adjust_current_prev = [int(x) for x in target.get()[1:-1].split(",")]
        target.set("按 Q 設置位置或按 C 取消")
        self.master.update()
        rx.just(1).subscribe(
            on_next=running,
            on_completed=lambda: self.master.after(5, on_task_done),
            scheduler=self.pool_scheduler
        )

    def copy_profile(self):
        profile_name = tk.StringVar()

        def done():
            if(n := profile_name.get()) != "":
                win.destroy()
                self.profileList.insert(0, n)
                with open(self.writepath, "r") as f:
                    d = json.load(f)
                d[n] = {
                    "rod": self.rod.get(),
                    "screen1": self.screen1.get(),
                    "screen2": self.screen2.get(),
                    "target": self.target.get()
                }
                with open(self.writepath, "w") as f:
                    json.dump(d, f)

        win = tk.Toplevel()
        win.wm_title("Profile Name")
        win.wm_geometry("300x100")

        tk.Entry(win, textvariable=profile_name,
                 font=self.font).grid(row=0, column=0)

        tk.Button(win, text="Okay", command=done,
                  font=self.font).grid(row=1, column=0)

    def start_fish(self):
        def do_task(_):
            play.Play().main(d)
             
        def on_task_done():
            pass

        with open(self.writepath, "r") as f:
            d = json.load(f)[self.current_profile_name.get()]
        print(d)
        rx.just(1).subscribe(
            on_next=do_task, 
            on_completed=lambda: self.master.after(5, on_task_done),
            scheduler=self.pool_scheduler
        )

if __name__ == "__main__":
    root = tk.Tk()
    autoFishGUI = AutoFishGUI(root)
    root.mainloop()
