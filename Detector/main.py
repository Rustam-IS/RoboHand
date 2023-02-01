import cv2
from mediapipe.python.solutions import (
    hands as detect, drawing_utils
)
from serial import Serial
from time import time


def scale(x, smn, smx, dmn, dmx):
    return (x - smn) * (dmx - dmn) / (smx - smn) + dmn


def dist(a, b):
    x = (a.x - b.x) ** 2
    y = (a.y - b.y) ** 2

    # cos(radians(abs(a.z / 0.17) * 45))
    # z = (a.z - b.z) ** 2
    return (x + y) ** (1 / 2)


cap = cv2.VideoCapture(0)
detector = detect.Hands(max_num_hands=1)

serial = Serial(
    port="COM28",
    baudrate=256000,
)

last = 0
cache = [0, 0, 0]

while True:
    _, image = cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # noqa
    h, w, c = image.shape

    hands = detector.process(image)
    hands = hands.multi_hand_landmarks  # noqa

    if hands:
        for hand in hands:
            elems = hand.landmark

            ind = dist(elems[5], elems[8])
            mid = dist(elems[9], elems[12])
            pik = dist(elems[13], elems[16])

            for n, finger in enumerate([ind, mid, pik]):
                port, data = [n + 2], [int(scale(finger, 0.02, 0.16, 255, 0))]
                if 0 <= data[0] <= 255 and abs(cache[n] - data[0]) > 16:
                    cache[n] = data[0]
                    # print(*port, finger)
                    serial.write(bytes(port))
                    serial.write(bytes(data))  # 0.02 0.14 -> 255 0

            drawing_utils.draw_landmarks(image, hand, detect.HAND_CONNECTIONS)

        cv2.imshow("Output", image)

    cv2.waitKey(1)
