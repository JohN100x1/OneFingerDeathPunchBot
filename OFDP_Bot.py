import cv2
import keypress
import numpy as np
import win32gui
from time import time, sleep
from windowcapture import get_screenshot

### TODO: brawling quicktime event is too slow
### TODO: chance of missing
### TODO: lightsaber rounds too fast

WINDOW_NAME = "One Finger Death Punch"
LEFT = 0x25
RIGHT = 0x27
THRESHOLD_ATK = 0.95
THRESHOLD_BRAWL = 0.7

LEFT_ATK_COLOUR = 9924188
RIGHT_ATK_COLOUR = 6052759

left_atk = cv2.imread("images//left_attack.png", cv2.IMREAD_UNCHANGED)
right_atk = cv2.imread("images//right_attack.png", cv2.IMREAD_UNCHANGED)
left_brawl = cv2.imread("images//left_brawl.png", cv2.IMREAD_UNCHANGED)
right_brawl = cv2.imread("images//right_brawl.png", cv2.IMREAD_UNCHANGED)

hwnd = win32gui.FindWindow(None, WINDOW_NAME)
hwndDC = win32gui.GetWindowDC(hwnd)

def rgbint2rgbtuple(RGBint):
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return (red, green, blue)

def colour_diff(c1, c2):
    # RBG values of colour c1
    r1 = (c1 >> 16) & 255
    g1 = (c1 >> 8) & 255
    b1 = c1 & 255
    # RBG values of colour c2
    r2 = (c2 >> 16) & 255
    g2 = (c2 >> 8) & 255
    b2 = c2 & 255
    # Calculate Euclidean percentage difference
    diff = (((r1-r2)**2+(g1-g2)**2+(b1-b2)**2)/195075)**0.5
    return diff

while True:
    
    #t0 = time()
    
    # Get Screenshot of Application window
    left_atk_pixels = np.array(get_screenshot(WINDOW_NAME, 549, 351, 552, 353))
    right_atk_pixels = np.array(get_screenshot(WINDOW_NAME, 727, 351, 730, 353))
    
    left_brawl_pixels = np.array(get_screenshot(WINDOW_NAME, 317, 281, 359, 496))
    right_brawl_pixels = np.array(get_screenshot(WINDOW_NAME, 916, 222, 958, 437))
    
    # Left attack detect
    left_atk_pixels = np.array(get_screenshot(WINDOW_NAME, 549, 351, 552, 353))
    left_atk_px = cv2.matchTemplate(left_atk_pixels, left_atk, cv2.TM_CCOEFF_NORMED)
    if cv2.minMaxLoc(left_atk_px)[1] >= THRESHOLD_ATK:
        print("Left Attack")
        keypress.hold_key(LEFT, 0.03)
    
    # Right attack detect
    right_atk_pixels = np.array(get_screenshot(WINDOW_NAME, 727, 351, 730, 353))
    right_atk_px = cv2.matchTemplate(right_atk_pixels, right_atk, cv2.TM_CCOEFF_NORMED)
    if cv2.minMaxLoc(right_atk_px)[1] >= THRESHOLD_ATK:
        print("Right Attack")
        keypress.hold_key(RIGHT, 0.03)
    
    # Left Brawl detect
    left_brawl_pixels = np.array(get_screenshot(WINDOW_NAME, 317, 281, 359, 496))
    left_brawl_res = cv2.matchTemplate(left_brawl_pixels, left_brawl, cv2.TM_CCOEFF_NORMED)
    if cv2.minMaxLoc(left_brawl_res)[1] >= THRESHOLD_BRAWL:
        print("Left Brawl")
        keypress.hold_key(LEFT, 0.03)
    
    # Right Brawl detect
    right_brawl_pixels = np.array(get_screenshot(WINDOW_NAME, 916, 222, 958, 437))
    right_brawl_res = cv2.matchTemplate(right_brawl_pixels, right_brawl, cv2.TM_CCOEFF_NORMED)
    if cv2.minMaxLoc(right_brawl_res)[1] >= THRESHOLD_BRAWL:
        print("Right Brawl")
        keypress.hold_key(RIGHT, 0.03)
    
    #cv2.imshow("Left Atk", left_atk_pixels)
    #cv2.imshow("Right Atk", right_atk_pixels)
    #cv2.imshow("Left Brawl", left_brawl_pixels)
    cv2.imshow("Right Brawl", right_brawl_pixels)
    
    # Escape key
    if cv2.waitKey(1) == ord("q"):
        break
    sleep(0.05)
    #print("FPS: {}".format(1/(time() - t0)))

# Stop Bot
win32gui.ReleaseDC(hwnd, hwndDC)
cv2.destroyAllWindows()
print("Bot Deactivated.")