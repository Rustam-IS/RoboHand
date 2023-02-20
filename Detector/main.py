import cv2
from mediapipe.python.solutions import (
    hands as detect, drawing_utils
)
from serial import Serial
from math import hypot, acos, pi


def scale(x, smn, smx, dmn, dmx):
    return (x - smn) * (dmx - dmn) / (smx - smn) + dmn


def vector(fp, sp):
    fx, fy, fz = fp.x, fp.y, fp.z
    sx, sy, sz = sp.x, sp.y, sp.z
    return [sx - fx, sy - fy, sz - fz]


def angle(fv, sv):
    fx, fy, fz = fv
    sx, sy, sz = sv

    fl = hypot(fx, fy, fz)
    sl = hypot(sx, sy, sz)

    if fl == 0 or sl == 0:
        return 90
    else:
        t = (fx * sx + fy * sy + fz * sz) / (fl * sl)
        return 0 if t > 1 or t < -1 else acos(t) * 180 / pi


def dist(a, b):
    x = (a.x - b.x) ** 2
    y = (a.y - b.y) ** 2

    # cos(radians(abs(a.z / 0.17) * 45))
    # z = (a.z - b.z) ** 2
    return (x + y) ** (1 / 2)


cap = cv2.VideoCapture(0)
detector = detect.Hands(max_num_hands=1)

serial = Serial(
    port="COM23",
    baudrate=256000,
)

cache = [0, 0, 0, 0, 0]

while True:
    _, image = cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # noqa
    h, w, c = image.shape

    hands = detector.process(image)
    hands = hands.multi_hand_landmarks  # noqa

    if not hands:
        continue

    for hand in hands:
        elems = hand.landmark

        # ind = angle(
        #     vector(elems[0], elems[5]),
        #     vector(elems[5], elems[6]),
        # )
        # mid = angle(
        #     vector(elems[0], elems[9]),
        #     vector(elems[9], elems[10]),
        # )
        # pik = angle(
        #     vector(elems[0], elems[13]),
        #     vector(elems[13], elems[14]),
        # )

        ind = dist(elems[5], elems[8])
        mid = dist(elems[9], elems[12])
        pik = dist(elems[13], elems[16])
        thy = dist(elems[2], elems[4])
        thx = abs(elems[4].x - elems[0].x)

        for n, (finger, rng) in enumerate([
            (thx, (0.060, 0.120)),
            (thy, (0.120, 0.060)),
            (ind, (0.030, 0.160)),
            (mid, (0.055, 0.165)),
            (pik, (0.060, 0.165)),
        ]):
            # 0.02 -> 0.16
            # 40 -> 9
            port, data = [n], [int(scale(finger, *rng, 255, 0))]
            # if port[0] == 0:
            #     print(data, finger)

            if 0 <= data[0] <= 255 and abs(cache[n] - data[0]) >= 32:
                cache[n] = data[0]
                try:
                    serial.write(bytes(port))
                    serial.write(bytes(data))
                    break
                except Exception as e:
                    print(e)

        drawing_utils.draw_landmarks(image, hand, detect.HAND_CONNECTIONS)

    cv2.imshow("Hands", image)
    cv2.waitKey(1)
