import json

from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from .models import Image

from .serializers import ImageSerializer

from fruit_grader.utilities.getPdfFromImages import get_pdf_from_images


def fruit_grader_form(request):
    return render(request, 'fruit-grader.html', {})


def get_grades_in_pdf(request):
    images = request.FILES.getlist('files[]')
    pdfPath = get_pdf_from_images(images)

    # return render(request, 'results.html', {})

    try:
        with open(pdfPath, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'filename=Fruit_Grades.pdf'
            return response
        pdfPath.close()
    except FileNotFoundError:
        raise Http404()


class GetGradesInPdf(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        images = request.data.getlist('files[]')

        for image in images:
            # res, score, grade = model_inference(image)
            # print(res.name, score, grade)
            imageName = image.name
            print(imageName)

        return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)
