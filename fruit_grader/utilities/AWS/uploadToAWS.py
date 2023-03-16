import os

from .uploadFileToAWS import upload_file_to_aws


def uploadToAWS(imagePathAbsolute, date, unique_token, gradingStatus):
    if gradingStatus == "graded":
        bucketName = "images-fruit-grader-graded"

    elif gradingStatus == "ungraded":
        bucketName = "images-fruit-grader-raw"

    fileName = os.path.basename(imagePathAbsolute)
    s3_file = date + "/" + unique_token + "/" + fileName

    upload_file_to_aws(imagePathAbsolute, bucketName, s3_file)
