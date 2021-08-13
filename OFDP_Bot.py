import cv2
from windowcapture import WindowCapture

WINDOW_NAME = "One Finger Death Punch"

wincap = WindowCapture(WINDOW_NAME)

while True:
    
    # Get screenshot
    cap = wincap.get_screenshot()
    
    # Display Image
    cv2.imshow("OFDP Img", cap)
    
    # Escape keys
    if cv2.waitKey(1) == ord("q"):
        break

# Stop Bot
cv2.destroyAllWindows()
print("Bot Deactivated.")