import os
from dotenv import load_dotenv
from PIL import Image
from pathlib import Path
from mss import mss
load_dotenv(dotenv_path=Path('./.env'))
monitor_index = int(os.getenv('monitor_index'))

with mss() as sct:
    sct_img = sct.grab(sct.monitors[monitor_index])
    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    img.show()