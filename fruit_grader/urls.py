from django.urls import path

from .views import fruit_grader_form, get_grades_in_pdf, GetGradesInPdf

urlpatterns = [
    path('fruit-grader', fruit_grader_form, name="fruit-grader"),
    path('api/get-grades-in-pdf', get_grades_in_pdf, name="get-grades-in-pdf"),
    # path('api/get-grades-in-pdf', GetGradesInPdf.as_view(), name="get-grades"),
]
