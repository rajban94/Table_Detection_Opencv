import cv2
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import os

def sortContours(cnts, method = 'left-to-right'):

    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    
    return (cnts, boundingBoxes)

def getProperTable(img):

    tableData = []
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshImg = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    threshImg = 255 - threshImg
    kernel = np.ones((5,191), np.uint8)
    morphImg = cv2.morphologyEx(threshImg, cv2.MORPH_CLOSE, kernel)
    contours = cv2.findContours(morphImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    contours, boundingBoxes = sortContours(contours, method='top-to-bottom')
    res = img.copy()
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if (h>300):
            image = cv2.rectangle(res, (x,y), (x+w, y+h), (0,0,0), 12)
            tableData.append((x, y, w, h))
    
    return image, tableData

def drawLines(img):
    
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
        cv2.drawContours(res, [c], -1, (0,0,0), 4)

    for c1 in cnts1:
        cv2.drawContours(res, [c1], -1, (0,0,0), 4)
    
    return res

def preProcess(img):

    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh, imgBin = cv2.threshold(grayImg, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    imgBin = 255 - imgBin

    return imgBin

def verticalLineDetect(invertedImg):

    kernel_len = np.array(invertedImg).shape[1] // 100
    vKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    vLines = cv2.dilate(cv2.erode(invertedImg, vKernel, iterations=3), vKernel, iterations=3)

    return vLines

def horizonalLineDetect(invertedImg):
    
    kernel_len = np.array(invertedImg).shape[1] // 100
    hKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
    hLines = cv2.dilate(cv2.erode(invertedImg, hKernel, iterations=3), hKernel, iterations=3)

    return hLines

def combineLines(img, vLines, hLines):

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    imgVH = cv2.addWeighted(vLines, 0.5, hLines, 0.5, 0.0)
    thresh, imgVH = cv2.threshold(imgVH, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # bitNOT = cv2.bitwise_not(cv2.bitwise_xor(grayImg, imgVH))
    
    return imgVH

def getBboxDtls(img, imgVH, tableDtls, imgPath):

    contours, hierarchy = cv2.findContours(imgVH, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, boundingBoxes = sortContours(contours, method="top-to-bottom")

    boxes = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if (h>50) and (h<500):
            boxes.append([x, y, w, h])

    bboxDtls = {}
    for tableBox1 in tableDtls:
        key = tableBox1
        values = []

        for tableBox2 in boxes:
            x2, y2, w2, h2 = tableBox2
            if tableBox1[0] <= x2 <= tableBox1[0] + tableBox1[2] and tableBox1[1] <= y2 <= tableBox1[1] + tableBox1[3]:
                values.append(tableBox2)
        bboxDtls[key] = values
    
    for key, values in bboxDtls.items():
        x_tab, y_tab, w_tab, h_tab = key
        cv2.rectangle(img, (x_tab, y_tab), (x_tab + w_tab, y_tab + h_tab), (255, 0, 0), 8)
        for box in values:
            x_box, y_box, w_box, h_box = box
            cv2.rectangle(img, (x_box, y_box), (x_box + w_box, y_box + h_box), (0, 255, 0), 4)

    cv2.imwrite(imgPath.replace('_rotated.jpg','_detected.jpg'),img)

    return bboxDtls

def detectMain(imgPath):
    
    cvImg = cv2.imread(imgPath)
    fileName = os.path.basename(imgPath).replace('_rotated.jpg', '')
    tableImg, tableRect = getProperTable(cvImg)
    tableImg = drawLines(tableImg)
    res = tableImg.copy()
    preImg = preProcess(tableImg)
    vLineImg = verticalLineDetect(preImg)
    hLineImg = horizonalLineDetect(preImg)
    combineLineImg = combineLines(res, vLineImg, hLineImg)
    bboxDtls = getBboxDtls(tableImg, combineLineImg, tableRect, imgPath)
    
    return bboxDtls, fileName, res