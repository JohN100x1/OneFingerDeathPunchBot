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
        
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y
        
        self.attack_w = self.w // 2
        self.attack_h = self.h // 3
        
    def get_attack_screenshot(self):
        # Get Window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(dcObj, self.attack_w, self.attack_h)
        cDC.SelectObject(bmp)
        cDC.BitBlt((0,0),(self.attack_w, self.attack_h) , dcObj, (self.cropped_x + self.w//4 , self.cropped_y + self.h//5), win32con.SRCCOPY)
    
        # Edit Bitmap
        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype="uint8")
        img.shape = (self.attack_h, self.attack_w, 4)
        img = np.ascontiguousarray(img[...,:3])
        
        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(bmp.GetHandle())
        
        return img
    
    def get_screen_position(self, pos):
        return pos[0] + self.offset_x, pos[1] + self.offset_y