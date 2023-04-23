import cv2
import cvzone
import numpy as np
import pickle

cap = cv2.VideoCapture("carPark.mp4")
width, height = 159 - 48, 193 - 145
with open("CarParkPos", "rb") as f:
    posList = pickle.load(f)
def checkParkingSpaces(imgPro):
    spaceCouter = 0
    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:y+height, x:x+width]
        count = cv2.countNonZero(imgCrop)
        if count < 900:
            color = (0, 255, 0)
            spaceCouter += 1
        else:
            color = (0, 0, 255)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1.5, thickness=2, offset=0)
        cv2.rectangle(img, (pos[0], pos[1]), (pos[0] + width, pos[1] + height), color, 2)
    cvzone.putTextRect(img, f"Free: {spaceCouter}/{len(posList)}", (100, 40), scale=1.5, thickness=2)

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                  25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    checkParkingSpaces(imgDilate)
    cv2.imshow("Video", img)
    cv2.waitKey(1)