import os, glob
from pdf2image import convert_from_path

def generateImage(pdfFile, imageDir):

    imgPath = []
    pdfImgPath = imageDir+'/'+os.path.basename(pdfFile).replace('.pdf','').replace('.PDF','')
    if not os.path.exists(pdfImgPath):
        os.makedirs(pdfImgPath)

    pdfImages = convert_from_path(pdfFile, dpi=500, poppler_path = './Dependencies\\poppler-0.68.0\\bin')
    imgName = os.path.basename(pdfFile).replace('.pdf','').replace('.PDF','')

    for i in range(len(pdfImages)):
        pdfImages[i].save(pdfImgPath + '/' + imgName + '_page' + str(i) + '.jpg', 'JPEG')
        imgPath.append(pdfImgPath + '/' + imgName + '_page' + str(i) + '.jpg')
    
    return imgPath