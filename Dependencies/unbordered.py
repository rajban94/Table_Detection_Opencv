import cv2
import numpy as np

def imageProcess(imgPath):
    cvImg = cv2.imread(imgPath)
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
        min_sublist_col = next(colBox for colBox in columnBoxes if colBox[0] == min_x)

        start_point_col = (min_sublist_col[0]+ 2 + min_sublist_col[2], y_new)
        end_point_col = (min_sublist_col[0] + min_sublist_col[2]+ 2, y_new + h_new)
        cv2.line(res, start_point_col, end_point_col, (0, 0, 0), 4)

        remainColBoxes.append(min_sublist_col)
        columnBoxes.remove(min_sublist_col)

    # Draw row grid lines
    while rowBoxes:
        max_y = max(rowBox[1] + rowBox[3] for rowBox in rowBoxes)
        min_sublist_row = next(rowBox for rowBox in rowBoxes if rowBox[1] + rowBox[3] == max_y)

        start_point_row = (x_new, min_sublist_row[1] + min_sublist_row[3] + 2)
        end_point_row = (x_new + w_new, min_sublist_row[1] + min_sublist_row[3] + 2)

        cv2.line(res, start_point_row, end_point_row, (0, 0, 0), 4)

        remainRowBoxes.append(min_sublist_row)
        rowBoxes.remove(min_sublist_row)

    cv2.imwrite(imgPath, res)

    return imgPath

# img = './test6.jpg'
# cellBbox = imageProcess(img)