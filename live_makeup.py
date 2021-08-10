import numpy as np
import cv2
from DigitalMakeup import Makeup

cap = cv2.VideoCapture(0)
MAKEUP_OBJ = Makeup()
my_filter = {"makeup": False, "chin": True, "bow_tie": False}

while True:
    ret, frame = cap.read()

    frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
    mod_frame = MAKEUP_OBJ.get_makeup(image=frame, filter=my_filter)
    # mod_frame = cv2.resize(mod_frame, (0, 0), fx=3, fy=3)
    cv2.imshow("Frame", mod_frame)
    ch = cv2.waitKey(1)
    if ch & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
