import os, glob
from pdf2image import convert_from_path

def generateImage(pdfFile, imageDir):

    '''
    Take PDF file as Input, create folder named
    with pdf name. Iterate through each page of PDF and convert it
    into image and dump it into the folder.
    '''

    pdfImgPath = imageDir+'/'+os.path.basename(pdfFile).replace('.pdf','').replace('.PDF','')
    if not os.path.exists(pdfImgPath):
        os.makedirs(pdfImgPath)

    pdfImages = convert_from_path(pdfFile, dpi=500, poppler_path = './Dependencies\\poppler-0.68.0\\bin')
    imgName = os.path.basename(pdfFile).replace('.pdf','').replace('.PDF','')

    for i in range(len(pdfImages)):
        pdfImages[i].save(pdfImgPath + '/' + imgName + '_page' + str(i) + '.jpg', 'JPEG')
    imgPath = pdfImgPath + '/' + imgName + '_page' + str(i) + '.jpg'
    return imgPath


    