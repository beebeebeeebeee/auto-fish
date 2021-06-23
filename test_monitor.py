import os
from dotenv import load_dotenv
from PIL import Image
from mss import mss
with mss() as sct:
    sct_img = sct.grab(sct.monitors[os.getenv('monitor_index')])
    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    img.show()