def scale(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;


import cv2
import mediapipe as mp
from serial import Serial


cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=4)
mpDraw = mp.solutions.drawing_utils

serial = Serial(
    port="COM29",
    baudrate=115200,
)

while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    # # checking whether a hand is detected
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 8:
                    a = lm.y
                    cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

                if id == 5:
                    b = lm.y
                    cv2.circle(image, (cx, cy), 25, (0, 0, 255), cv2.FILLED)

            if 0.04 < b - a < 0.2:
                serial.write(bytes([2]))
                serial.write(bytes([int(scale(b - a, 0.04, 0.2, 255, 0))]))  # 0.04 0.2 -> 255 0

            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Output", image)
    cv2.waitKey(1)
