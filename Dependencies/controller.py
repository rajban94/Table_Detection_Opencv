from imageconversion import *
from rotateimage import *
from tabledetect import *
from tableextract import *
from unbordered import *
import easyocr
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

def main(ocr, pdfFile, outPathImg, outPathExcel):
    print(f"*********************** IMAGE CONVERSION STARTED FOR {os.path.basename(pdfFile)} ***********************\n")
    imagePath = generateImage(pdfFile, outPathImg)
    print(f"*********************** IMAGE CONVERSION COMPLETED FOR {os.path.basename(pdfFile)} *********************\n")

    for eachImgPath in imagePath:
        print(f"*********************** IMAGE ROTATION STARTED FOR {os.path.basename(eachImgPath)} *******************\n")
        rotateImgPath = rotateMain(eachImgPath)
        print(f"*********************** IMAGE ROTATION COMPLETED FOR {os.path.basename(eachImgPath)} *****************\n")

        print(f"*********************** IMAGE DETECTION STARTED FOR {os.path.basename(eachImgPath)} ******************\n")
        try:
            bboxDtls, filename, cvImg = detectMain(rotateImgPath)
        except:
            unborderedPath = imageProcess(rotateImgPath)
            bboxDtls, filename, cvImg = detectMain(unborderedPath)
        print(f"*********************** IMAGE DETECTION COMPLETED FOR {os.path.basename(eachImgPath)} ****************\n")

        print(f"*********************** IMAGE EXTRACTION STARTED FOR {os.path.basename(eachImgPath)} *****************\n")
        outCommand = extractMain(ocr, bboxDtls, cvImg, outPathExcel, filename)
        print(f"*********************** IMAGE EXTRACTION COMPLETED FOR {os.path.basename(eachImgPath)} ***************\n")

    print(outCommand)

if __name__ == '__main__':

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

    for x in range(len(pdfDir)):
        main(reader, pdfDir[x], outImgFolder, outExcelFolder)