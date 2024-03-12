from imageconversion import *
from rotateimage import *
from tabledetect import *
from tableextract import *
from formatexcel import *
import easyocr
import time
import concurrent.futures
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

def processImage(ocr, eachImgPath, outPathExcel):

    print(f"*********************** IMAGE ROTATION STARTED FOR {os.path.basename(eachImgPath)} *******************\n")
    rotateImgPath = rotateMain(eachImgPath)
    print(f"*********************** IMAGE ROTATION COMPLETED FOR {os.path.basename(eachImgPath)} *****************\n")

    print(f"*********************** IMAGE DETECTION STARTED FOR {os.path.basename(eachImgPath)} ******************\n")
    bboxDtls, filename, cvImg = detectMain(rotateImgPath)
    print(f"*********************** IMAGE DETECTION COMPLETED FOR {os.path.basename(eachImgPath)} ****************\n")

    print(f"*********************** IMAGE EXTRACTION STARTED FOR {os.path.basename(eachImgPath)} *****************\n")
    outCommand = extractMain(ocr, bboxDtls, cvImg, outPathExcel, filename)
    print(f"*********************** IMAGE EXTRACTION COMPLETED FOR {os.path.basename(eachImgPath)} ***************\n")

    print(outCommand)

def main(pdfFile, outPathImg):

    print(f"*********************** IMAGE CONVERSION STARTED FOR {os.path.basename(pdfFile)} ***********************\n")
    imagePath = generateImage(pdfFile, outPathImg)
    print(f"*********************** IMAGE CONVERSION COMPLETED FOR {os.path.basename(pdfFile)} *********************\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(imagePath)) as executor:
        for eachImgPath in imagePath:
            executor.submit(processImage, reader, eachImgPath, outExcelFolder)

    
if __name__ == '__main__':

    startTime = time.time()

    reader = easyocr.Reader(['en'], gpu=False)
    pdfPath = './Input'
    outImgFolder = './Images'
    outExcelFolder = './Output'

    if not os.path.exists(outImgFolder):
        os.makedirs(outImgFolder)
    
    if not os.path.exists(outExcelFolder):
        os.makedirs(outExcelFolder)

    pdfDir = glob.glob(pdfPath + '/*')
    pdfDir = [pdf for pdf in pdfDir if pdf.endswith('.pdf') or pdf.endswith('.PDF')]

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(pdfDir)) as executor:
        for x in range(len(pdfDir)):
            executor.submit(main, pdfDir[x], outImgFolder)
    
    mergeExcels(outExcelFolder)

    endTime = time.time()
    totalTime = (endTime - startTime)

    print(f"********* TOTAL TIME TAKEN {str(totalTime)}**************")