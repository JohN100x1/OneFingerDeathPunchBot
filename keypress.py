import win32api
from time import sleep

def hold_key(key, hold_time):
    win32api.keybd_event(key, 0, 0x00)
    sleep(hold_time)
    win32api.keybd_event(key, 0, 0x02)