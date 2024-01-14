from django.urls import path
from .import views
from . import imports

urlpatterns = [
    path('import-student-data', imports.import_student_data, name='import-student-data'),
    path('import-courses-data', imports.import_courses_data, name='import-courses-data'),
    path('import-question-data', imports.import_question_data, name='import-question-data'),
    path('verify-student-data', imports.verify_data, name='verify-student-data'),
    path('verify-course-data', imports.verify_data1, name='verify-course-data'),
    path('verify-question-data', imports.verify_data2, name='verify-question-data'),
    
    
     
    path('calculate-marks', views.calculate_marks_view, name='calculate-marks'),
    path('excel-download', views.excel_download, name='excel-download'),
    path('excel-download1', views.excel_download1, name='excel-download1'),
    path('excel-download2', views.excel_download2, name='excel-download2'),
    
    
    
    
]