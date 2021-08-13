import cv2
import keypress
from windowcapture import WindowCapture

### ISSUES: targetting should choose closer enemy
### TODO: brawler detection

WINDOW_NAME = "One Finger Death Punch"
THRESHOLD_ATK = 0.8
THRESHOLD_BRAWL = 0.9

wincap = WindowCapture(WINDOW_NAME)

left_attack = cv2.imread("images//left_attack.png", cv2.IMREAD_UNCHANGED)
right_attack = cv2.imread("images//right_attack.png", cv2.IMREAD_UNCHANGED)

left_brawl = cv2.imread("images//left_brawl.png", cv2.IMREAD_UNCHANGED)
right_brawl = cv2.imread("images//right_brawl.png", cv2.IMREAD_UNCHANGED)

tick = 0

while True:
    
    # Get screenshots
    #cap = wincap.get_screenshot()
    attack_cap = wincap.get_attack_screenshot()
    #brawl_cap = wincap.get_brawler_screenshot()
    
    # Detection
    left_attack_result = cv2.matchTemplate(attack_cap, left_attack, cv2.TM_CCOEFF_NORMED)
    right_attack_result = cv2.matchTemplate(attack_cap, right_attack, cv2.TM_CCOEFF_NORMED)
    
    left_brawl_result = cv2.matchTemplate(attack_cap, left_brawl, cv2.TM_CCOEFF_NORMED)
    right_brawl_result = cv2.matchTemplate(attack_cap, right_brawl, cv2.TM_CCOEFF_NORMED)
    
    _, left_attack_val, _, _ = cv2.minMaxLoc(left_attack_result)
    _, right_attack_val, _, _ = cv2.minMaxLoc(right_attack_result)
    
    _, left_brawl_val, _, _ = cv2.minMaxLoc(left_brawl_result)
    _, right_brawl_val, _, _ = cv2.minMaxLoc(right_brawl_result)
    
    # Perform actions
    if tick % 2:
        if left_attack_val >= THRESHOLD_ATK:
            print("Left Attack")
            keypress.hold_key("left", 0.001)
        elif right_attack_val >= THRESHOLD_ATK:
            print("Right Attack")
            keypress.hold_key("right", 0.001)
    else:
        if right_attack_val >= THRESHOLD_ATK:
            print("Right Attack")
            keypress.hold_key("right", 0.001)
        elif left_attack_val >= THRESHOLD_ATK:
            print("Left Attack")
            keypress.hold_key("left", 0.001)
    # Brawl press
    if left_brawl_val >= THRESHOLD_BRAWL:
            print("Left Brawl")
            keypress.hold_key("left", 0.001)
    elif right_brawl_val >= THRESHOLD_BRAWL:
            print("Right Brawl")
            keypress.hold_key("right", 0.001)
    
    # Display Image
    cv2.imshow("OFDP Img", attack_cap)
    #cv2.imshow("Brawler Img", brawl_cap)
    
    # Escape keys
    if cv2.waitKey(1) == ord("q"):
        break
    
    tick += 1

# Stop Bot
cv2.destroyAllWindows()
print("Bot Deactivated.")