import cv2
import numpy as np

def isLineLntersecting_box(startPoint, endPoint, box):
    x, y, w, h = box
    rect1 = [(startPoint[0], startPoint[1]), (endPoint[0], endPoint[1])]
    rect2 = [(x, y), (x + w, y + h)]

    if (rect1[0][0] > rect2[1][0] or rect1[1][0] < rect2[0][0] or
        rect1[0][1] > rect2[1][1] or rect1[1][1] < rect2[0][1]):
        return False
    else:
        return True

def omitLines(img):
    
    res = img.copy()
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshImg = cv2.threshold(grayImg, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    vKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    rmVertical = cv2.morphologyEx(threshImg, cv2.MORPH_OPEN, vKernel, iterations=2)

    hKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    rmHorizontal = cv2.morphologyEx(threshImg, cv2.MORPH_OPEN, hKernel, iterations=2)

    cnts = cv2.findContours(rmVertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    cnts1 = cv2.findContours(rmHorizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts1 = cnts1[0] if len(cnts1) == 2 else cnts1[1]

    for c in cnts:
        cv2.drawContours(res, [c], -1, (255,255,255), 4)

    for c1 in cnts1:
        cv2.drawContours(res, [c1], -1, (255,255,255), 4)
    
    return res

def imageProcess(imgPath):
    
    cvImg = cv2.imread(imgPath)
    cvImg = omitLines(cvImg)
    res = cvImg.copy()
    grayImg = cv2.cvtColor(cvImg, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = np.ones((5, 80), np.uint8)
    dilateImg = cv2.dilate(thresh, kernel, iterations=1)
    contours = cv2.findContours(dilateImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    allBoxes = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if h > 20:
            x, y, w, h = x, y - 2, w, h + 4
            # cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)
            allBoxes.append([x, y, w, h])

    x_min = [min([box[0] - 5 for box in allBoxes]), min([box[1] - 5 for box in allBoxes])]
    y_max = [max([box[0] + box[2] + 5 for box in allBoxes]), max([box[1] + box[3] + 5 for box in allBoxes])]

    table_area = x_min + y_max
    x1, y1, w1, h1 = table_area
    cv2.rectangle(res, (x1, y1), (w1, h1), (0, 0, 0), 4)

    x_new = x_min[0]
    y_new = x_min[1]
    w_new = y_max[0] - x_min[0]
    h_new = y_max[1] - x_min[1]

    rowBoxes = allBoxes.copy()
    remainRowBoxes = []
    columnBoxes = allBoxes.copy()
    remainColBoxes = []

    # Draw column grid lines at the bottom
    while columnBoxes:

        min_x = min(colBox[0] for colBox in columnBoxes)
        minSublistCol = next(colBox for colBox in columnBoxes if colBox[0] == min_x)

        startPointCol = (minSublistCol[0]+ 2 + minSublistCol[2], y_new)
        endPointCol = (minSublistCol[0] + minSublistCol[2]+ 2, y_new + h_new)

        isIntersectCol = any(isLineLntersecting_box(startPointCol, endPointCol, colBox) for colBox in allBoxes)
        if not isIntersectCol:
            cv2.line(res, startPointCol, endPointCol, (0, 0, 0), 4)
            remainColBoxes.append(minSublistCol)
        columnBoxes.remove(minSublistCol)

    # Draw row grid lines
    while rowBoxes:
        max_y = max(rowBox[1] + rowBox[3] for rowBox in rowBoxes)
        minSublistRow = next(rowBox for rowBox in rowBoxes if rowBox[1] + rowBox[3] == max_y)

        startPointRow = (x_new, minSublistRow[1] + minSublistRow[3] + 2)
        end_point_row = (x_new + w_new, minSublistRow[1] + minSublistRow[3] + 2)

        isIntersectRow = any(isLineLntersecting_box(startPointRow, end_point_row, rowBox) for rowBox in allBoxes)
        if not isIntersectRow:
            cv2.line(res, startPointRow, end_point_row, (0, 0, 0), 4)
            remainRowBoxes.append(minSublistRow)
        rowBoxes.remove(minSublistRow)

    cv2.imwrite(imgPath, res)

    return imgPath