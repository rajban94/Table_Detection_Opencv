import cv2
import numpy as np
from scipy.ndimage import interpolation as inter

def findScore(arr, angle):
    data = inter.rotate(arr, angle, reshape=False, order=0)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score


def findNormalRotation(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ht, wd = img.shape[:2]
    pix = ~img
    bin_img = 1 - (pix.reshape((ht, wd)) / 255.0)
    delta = 0.5
    limit = 6
    angles = np.arange(-limit, limit + delta, delta)
    scores = []
    for angle in angles:
        hist, score = findScore(bin_img, angle)
        scores.append(score)

    best_score = max(scores)
    best_angle = angles[scores.index(best_score)]
    return best_angle

def rotateImage(img, angle):
    h, w = img.shape[:2]
    center = (w //2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w,h), 
                             flags = cv2.INTER_CUBIC, borderMode = cv2.BORDER_REPLICATE)
    return rotated

def alignImage(imagePath):
    cvImage = cv2.imread(imagePath)
    res = cvImage.copy()
    normRotation = findNormalRotation(cvImage)
    rotatedImage = rotateImage(res, normRotation)
    return rotatedImage

def rotateMain(imagePath):
    correctedImage = alignImage(imagePath)
    rotatePath = imagePath.replace('.jpg','_rotated.jpg')
    cv2.imwrite(imagePath.replace('.jpg','_rotated.jpg'), correctedImage)
    return rotatePath