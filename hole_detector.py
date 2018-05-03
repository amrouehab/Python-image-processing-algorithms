import cv2
import numpy as np


def getPosOfThirdAndFourthPoints(y1, x1, y2, x2):
    r = int(round((x2 - x1) / 2))
    xc = x2 - r
    yc = y2
    x3 = int(round(r / np.sqrt(2)))
    y3 = x3
    x4 = -x3
    y4 = -y3
    x3 = x3 + xc
    y3 = y3 + yc
    x4 = x4 + xc
    y4 = y4 + yc

    return [x4, y4], [x3, y3], r, [xc, yc]


def checkIfthosPointsIsOnACircle(p3, p4, boundary):
    height, width = boundary.shape[:2]
    i = -2
    point3IsOnCircle = False
    if p3[0] + 2 < width and p4[0] + 2 < width and p4[1]<height and p3[1]< height:
        row = boundary[p3[1]]
        while i != 2:
            row_value = row[p3[0] + i]
            if row_value == 255:
                point3IsOnCircle = True
                break
            else:
                i = i + 1
    if point3IsOnCircle:
        row = boundary[p4[1]]
        while i != 2:
            row_value = row[p4[0] + i]
            if row_value == 255:
                return True
            else:
                i = i + 1

    return False


def getCircles(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    kernel = np.array([[0, 1, 0],
                       [1, 1, 1],
                       [0, 1, 0],
                       ],np.uint8)

    ret, img_binary = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
    erode = cv2.erode(~img_binary, kernel)
    boundary = (~img_binary) - erode
    boundary = cv2.dilate(boundary, kernel)
    cv2.imshow('image', boundary)
    cv2.imshow('image3', ~img_binary)


    prev_column = 0
    RowIndex = 0
    ColumnIndex = 0
    p1 = [0, 0]
    p1IsObtained = False
    Circles = []
    Circles_count = 0
    for ROW in boundary:
        for colVal in ROW:
            if colVal == 255:
                if p1IsObtained:
                    p2 = [RowIndex, ColumnIndex]
                    p3, p4, r, C = getPosOfThirdAndFourthPoints(p1[0], p1[1], p2[0], p2[1])
                    CircleIsDetected = checkIfthosPointsIsOnACircle(p3, p4, boundary)
                    if CircleIsDetected:
                        Circles.insert(Circles_count, [C, r])
                        Circles_count = Circles_count + 1
                    p1IsObtained = False

                prev_column = 255

            else:
                if prev_column == 255:
                    p1 = [RowIndex, ColumnIndex - 1]
                    p1IsObtained = True
                prev_column = 0
            ColumnIndex = ColumnIndex + 1
        RowIndex = RowIndex + 1  # increment the ROW index
        p1IsObtained = False

        ColumnIndex = 0

    return Circles


img = cv2.imread('wood.jpg')
cv2.imshow('original', img)

circles = getCircles(img)

for circle in circles:
    center = circle[0]
    r = circle[1]
    cv2.circle(img, (center[0], center[1]), r, (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(img, (center[0], center[1]), 1, (0, 0, 255), 3)
cv2.imshow('detected circles', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
