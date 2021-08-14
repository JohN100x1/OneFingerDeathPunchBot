import cv2
import keypress
import numpy as np
from windowcapture import get_screenshot

### TODO: brawling quicktime event is too slow
### TODO: chance of missing due to simulateous left/right attack causing the enemy to be out of range (need re-detection)

WINDOW_NAME = "One Finger Death Punch"
THRESHOLD_ATK = 0.95
THRESHOLD_BRAWL = 0.7

left_atk = cv2.imread("images//left_attack.png", cv2.IMREAD_UNCHANGED)
right_atk = cv2.imread("images//right_attack.png", cv2.IMREAD_UNCHANGED)
left_brawl = cv2.imread("images//left_brawl.png", cv2.IMREAD_UNCHANGED)
right_brawl = cv2.imread("images//right_brawl.png", cv2.IMREAD_UNCHANGED)

tick = 0

while True:
    
    cap = np.array(get_screenshot(WINDOW_NAME))
    cap = cv2.cvtColor(cap, cv2.COLOR_RGB2BGR)
    
    # Image match calculation
    left_atk_res = cv2.matchTemplate(cap[335:351, 393:400, :], left_atk, cv2.TM_CCOEFF_NORMED)
    right_atk_res = cv2.matchTemplate(cap[335:351, 880:887, :], right_atk, cv2.TM_CCOEFF_NORMED)
    left_brawl_res = cv2.matchTemplate(cap[281:496, 317:359, :], left_brawl, cv2.TM_CCOEFF_NORMED)
    right_brawl_res = cv2.matchTemplate(cap[222:437, 916:958, :], right_brawl, cv2.TM_CCOEFF_NORMED)
    
    print(cv2.minMaxLoc(left_brawl_res)[1], cv2.minMaxLoc(right_brawl_res)[1])
    if cv2.minMaxLoc(left_atk_res)[1] >= THRESHOLD_ATK:
        print("Left Attack")
        keypress.hold_key("left", 0.01)
    if cv2.minMaxLoc(right_atk_res)[1] >= THRESHOLD_ATK:
        print("Right Attack")
        keypress.hold_key("right", 0.01)
    if cv2.minMaxLoc(left_brawl_res)[1] >= THRESHOLD_BRAWL:
        print("Left Brawl")
        keypress.hold_key("left", 0.01)
    if cv2.minMaxLoc(right_brawl_res)[1] >= THRESHOLD_BRAWL:
        print("Right Brawl")
        keypress.hold_key("right", 0.01)
    
    #cv2.imshow("Left Atk", cap[335:351, 393:400, :])
    #cv2.imshow("Right Atk", cap[335:351, 880:887, :])
    cv2.imshow("Left Brawl", cap[281:496, 317:359, :])
    cv2.imshow("Right Brawl", cap[222:437, 916:958, :])
    
    # Escape keys
    if cv2.waitKey(1) == ord("q"):
        break

# Stop Bot
cv2.destroyAllWindows()
print("Bot Deactivated.")