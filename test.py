import keyboard
from pynput.mouse import Button, Controller
mouse = Controller()

input("Press Enter to continue...")
x,y = mouse.position
print("[%s, %s]" % (round(x),round(y)))