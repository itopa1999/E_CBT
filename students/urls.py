from django.urls import path
from .import views


urlpatterns = [
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('demo', views.pre_video, name='demo'),
    path('exam-mode/<int:pk>', views.exam_mode, name='exam-mode'),
    path('exam-details/<int:pk>', views.exam_details, name='exam-details'),
    path('mark/<int:pk>', views.mark, name='mark'),
    path('student-course-mark', views.student_course_mark, name='student-course-mark'),
    path('demo', views.pre_video, name='demo'),

]