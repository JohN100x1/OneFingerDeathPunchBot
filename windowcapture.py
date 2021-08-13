import numpy as np
import win32gui, win32ui, win32con

class WindowCapture:
    
    def __init__(self, window_name):
        # Find the window from name
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception("Window not found: " + window_name)
        
        # Get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]
        
        # Remove Border and shift cropping
        border_pixels = 8
        titlebar_pixels = 30
        self.w -= border_pixels * 2
        self.h -= titlebar_pixels + titlebar_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels
        
        
    def get_screenshot(self):
        # Get Window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(bmp)
        cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
    
        # Edit Bitmap
        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype="uint8")
        img.shape = (self.h, self.w, 4)
        img = np.ascontiguousarray(img[...,:3])
        
        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(bmp.GetHandle())
        
        return img