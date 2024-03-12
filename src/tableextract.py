import cv2
import os
import numpy as np
import pandas as pd

def getRowsCols(box, height, mean):

    row = []
    column = []
    j = 0

    for i in range(len(box)):
        if (i == 0):
            column.append(box[i])
            previous = box[i]
        else:
            if (box[i][1] <= previous[1] + mean / 2):
                column.append(box[i])
                previous = box[i]
                if (i == len(box) - 1):
                    row.append(column)
            else:
                row.append(column)
                column = []
                previous = box[i]
                column.append(box[i])

    countCol = 0
    index = 0
    for i in range(len(row)):
        current = len(row[i])
        if current > countCol:
            countCol = current
            index = i

    center = [int(row[i][j][0] + row[i][j][2] / 2) for j in range(len(row[i])) if row[0]]
    center = np.array(center)
    center.sort()

    finalBoxes = []
    for i in range(len(row)):
        lis = []
        for k in range(countCol):
            lis.append([])
        for j in range(len(row[i])):
            diff = abs(center - (row[i][j][0] + row[i][j][2] / 4))
            minimum = min(diff)
            indexing = list(diff).index(minimum)
            lis[indexing].append(row[i][j])
        finalBoxes.append(lis)
    
    return finalBoxes, row, countCol

def extractBoxes(reader, finalBoxes, img):

    outer = []
    for i in range(len(finalBoxes)):
        for j in range(len(finalBoxes[i])):
            inner = ''
            if (len(finalBoxes[i][j]) == 0):
                outer.append(' ')
            else:
                for k in range(len(finalBoxes[i][j])):
                    y, x, w, h = finalBoxes[i][j][k][0], finalBoxes[i][j][k][1], finalBoxes[i][j][k][2], finalBoxes[i][j][k][3]
                    finalImg = img[x:x + h, y:y + w]
                    _, imgCrop = cv2.threshold(cv2.cvtColor(finalImg, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                    out = reader.readtext(imgCrop, detail=0, paragraph=False)
                    for text in out:
                        inner = inner + text
                outer.append(inner)
    
    return outer

def dataframeGeneration(texts, rows, columnCount):

    arr = np.array(texts)
    dataFrame = pd.DataFrame(arr.reshape(len(rows), columnCount))
    data = dataFrame.style.set_properties(align='left')

    return data

def excelGeneration(fileName, dataFrames):

    with pd.ExcelWriter(fileName) as writer:
        for i, df in enumerate(dataFrames, start=1):
            sheetName = f"Sheet{i}"
            df.to_excel(writer, sheet_name=sheetName, index=False)

def extractMain(ocrEngine, tablebboxDtls, cvImg, outPath, fileName):

    allDataframes = []
    for tabs, boxes in tablebboxDtls.items():
        heights = [boxes[i][3] for i in range(len(boxes))]
        mean = np.mean(heights)
        allSortedBoxes, rows, cols = getRowsCols(boxes, heights, mean)
        extractedData = extractBoxes(ocrEngine, allSortedBoxes, cvImg)
        eachDataDf = dataframeGeneration(extractedData, rows, cols)
        allDataframes.append(eachDataDf)
    
    folder = fileName.split('_page')[0]
    if not os.path.exists(outPath + "/" + folder):
        os.makedirs(outPath + "/" + folder)

    excelGeneration(outPath + "/" + folder + "/" + fileName + '.xlsx', allDataframes)
    fSting = f"EXCEL GENETAION COMPLETED FOR {fileName.split('.xlsx')[0]} IN {outPath.replace('./','')} FOLDER\n"

    return fSting