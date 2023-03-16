import os
import cv2

from fpdf import FPDF  # fpdf class
from datetime import date

from segritech import settings
from .imageHandling import storeImageToLocal, deleteFileFromLocal, addGradesToImageName, getPathAbsolute
from .AWS.uploadToAWS import uploadToAWS
from ..GradingModel.pomAI import model_inference


def addImageAndGradesToPdf(inputImageName, pdf, gradedImagePathAbsolute, score, grade):
    image = cv2.imread(gradedImagePathAbsolute)
    inputImageHeight, inputImageWidth = image.shape[:2]

    pageWidth = 21.0
    marginForPadding = 1.0
    marginForGrades = 7.5

    # Adding image
    imageWidth = pageWidth - marginForPadding * 2
    imageHeight = imageWidth * inputImageHeight / inputImageWidth

    pageHeight = imageHeight + marginForGrades + marginForPadding

    pdf.add_page(format=(pageWidth, pageHeight))
    pdf.image(gradedImagePathAbsolute, marginForPadding, marginForPadding, w=imageWidth, h=imageHeight)

    # Adding filename
    pdf.set_xy(0, marginForPadding + imageHeight + 1)
    pdf.set_font('Arial', 'B', 30)
    pdf.set_text_color(218, 65, 103)
    pdf.cell(w=pageWidth, align='C', txt=inputImageName, border=0)

    # Adding score
    pdf.set_xy(0, marginForPadding + imageHeight + 3)
    pdf.set_font('Arial', 'B', 30)
    pdf.set_text_color(92, 184, 116)
    pdf.cell(w=pageWidth, align='C', txt="Score = " + str(score) + "%", border=0)

    # Adding grade
    pdf.set_xy(0, marginForPadding + imageHeight + 5)
    pdf.set_font('Arial', 'B', 30)
    pdf.set_text_color(63, 136, 197)
    pdf.cell(w=pageWidth, align='C', txt="Grade = " + str(grade), border=0)


def generateUniqueToken():
    import uuid
    return str(uuid.uuid4())


def get_pdf_from_images(images):
    unique_token = generateUniqueToken()
    today = str(date.today())

    pdf = FPDF(unit="cm")

    for image in images:
        inputImageName = storeImageToLocal(image)
        imagePathAbsolute = getPathAbsolute(inputImageName)

        res, score, grade = model_inference(imagePathAbsolute)
        uploadToAWS(imagePathAbsolute, today, unique_token, "ungraded")
        deleteFileFromLocal(imagePathAbsolute)

        gradedImagePathAbsolute = addGradesToImageName(imagePathAbsolute, score, grade)
        cv2.imwrite(gradedImagePathAbsolute, res)
        uploadToAWS(gradedImagePathAbsolute, today, unique_token, "graded")

        addImageAndGradesToPdf(inputImageName, pdf, gradedImagePathAbsolute, score, grade)
        deleteFileFromLocal(gradedImagePathAbsolute)

    pdfName = unique_token + '.pdf'
    pdfPath = os.path.join(settings.MEDIA_ROOT, pdfName)
    pdf.output(pdfPath, 'F')

    return pdfPath
