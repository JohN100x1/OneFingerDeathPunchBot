import pydirectinput
from time import time

def hold_key(key, hold_time):
    t0 = time()
    while time() - t0 < hold_time:
        pydirectinput.press(key)