import cv2
import pickle

try:
    with open("CarParkPos", "rb") as f:
        posList = pickle.load(f)
except:
    posList = []
width, height = 159 - 48, 193 - 145
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            if pos[0] < x < pos[0] + width and pos[1] < y < pos[1] + height:
                posList.pop(i)
    with open("CarParkPos", "wb") as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread("carParkImg.png")
    for pos in posList:
        cv2.rectangle(img, (pos[0], pos[1]), (pos[0] + width, pos[1] + height), (0, 255, 0), 2)
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouseClick)
    cv2.waitKey(1)