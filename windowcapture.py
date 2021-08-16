import win32gui
import win32ui
import win32con
import numpy as np


def get_screenshot(window_name, x1, y1, x2, y2):
    hwnd = win32gui.FindWindow(None, window_name)

    left, top, right, bot = win32gui.GetClientRect(hwnd)
    border_px = 8
    titlebar_px = 31
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0,0),(x2-x1, y2-y1) , mfcDC, (border_px+x1,titlebar_px+y1), win32con.SRCCOPY)

    bmpstr = saveBitMap.GetBitmapBits(True)
    
    img = np.fromstring(bmpstr, dtype="uint8")
    img.shape = (h, w, 4)
    img = img[:(y2-y1),:(x2-x1),:3]
    img = np.ascontiguousarray(img)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    
    return img
