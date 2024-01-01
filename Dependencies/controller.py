from imageconversion import *
from rotateimage import *
from tabledetect import *
from tableextract import *
import easyocr
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

def main(ocr, pdfFile, outPathImg, outPathExcel):
    print(f"*********************** IMAGE CONVERSION STARTED FOR {os.path.basename(pdfFile)} ***********************\n")
    imagePath = generateImage(pdfFile, outPathImg)
    print(f"*********************** IMAGE CONVERSION COMPLETED FOR {os.path.basename(pdfFile)} *********************\n")

    print(f"*********************** IMAGE ROTATION STARTED FOR {os.path.basename(imagePath)} *******************\n")
    rotateImgPath = rotateMain(imagePath)
    print(f"*********************** IMAGE ROTATION COMPLETED FOR {os.path.basename(imagePath)} *****************\n")

    print(f"*********************** IMAGE DETECTION STARTED FOR {os.path.basename(imagePath)} ******************\n")
    bboxDtls, filename, cvImg = detectMain(rotateImgPath)
    print(f"*********************** IMAGE DETECTION COMPLETED FOR {os.path.basename(imagePath)} ****************\n")

    print(f"*********************** IMAGE EXTRACTION STARTED FOR {os.path.basename(imagePath)} *****************\n")
    outCommand = extractMain(ocr, bboxDtls, cvImg, outPathExcel, filename)
    print(f"*********************** IMAGE EXTRACTION COMPLETED FOR {os.path.basename(imagePath)} ***************\n")

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