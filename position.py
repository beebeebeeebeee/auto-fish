from pynput.mouse import Button, Controller
import pyautogui
from mss import mss
from PIL import Image

mouse = Controller()
import time

crop_factor = 1

with mss() as sct:
    sct_img = sct.grab(sct.monitors[1])
    if(sct_img.width > pyautogui.size().width):
        crop_factor = sct_img.width/pyautogui.size().width

def getColor(x, y):
    with mss() as sct:
        sct_img = sct.grab(sct.monitors[1])
        x = x*crop_factor
        y = y*crop_factor
        # Convert to PIL.Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return img.load()[x, y]

while 1:
    x,y = mouse.position
    PIXEL = pyautogui.screenshot(
        region=(
            x, y, 1, 1
        )
    )
    print("[%s, %s]" % (round(x),round(y)))
    print(pyautogui.size())
    print(pyautogui.position())
    print(PIXEL.getcolors())
    print(getColor(x,y))
    print("===========================")
    # time.sleep(0.1)