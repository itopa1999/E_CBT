from django.urls import path, include
from .import views


urlpatterns = [
    path('login/', views.login_user, name='login_admin'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('changepassword', views.changepassword, name='changepassword'),
    
    path('decline', views.decline, name='decline'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    
    
    path('all-student', views.all_student, name='all-student'),
    path('delete-student', views.del_student, name='delete-student'),
    path('delete-student1/<int:pk>', views.del_student1, name='delete-student1'),
    path('add-student', views.add_student, name='add-student'),
    path('del-all-student', views.del_all_student, name='del-all-student'),
    
    
    
    path('add-department', views.add_department, name='add-department'),
    path('department', views.department, name='department'),
    path('delete-department/<int:pk>', views.del_department, name='delete-department'),
    
    
    path('import-courses', views.import_courses, name='import-courses'),
    path('add-course', views.add_course, name='add-course'),
    path('course', views.course, name='course'),
    path('delete-course/<int:pk>', views.del_course, name='delete-course'),
    path('del-all-courses', views.del_all_courses, name='del-all-courses'),
    
    
    path('question', views.question, name='question'),
    path('question-details/<int:pk>', views.question_details, name='question-details'),
    path('add-question', views.add_question, name='add-question'),
    path('import-question', views.import_question, name='import-question'),
    path('del-all-question', views.del_all_question, name='del-all-question'),
    path('del-course-question/<str:name>', views.del_course_question, name='del-course-question'),
    
    
    path('count_mode/', views.count_mode, name='count_mode'),
    path('import-students', views.import_students, name='import-students'),
    

    path('all_results', views.all_results, name='all_results'),
    path('admin-view-mark/<int:pk>', views.admin_view_mark, name='admin-view-mark'),
    
    path('del-all-results', views.del_all_results, name='del-all-results'),
    path('del-result/<int:pk>', views.del_result, name='del-result'),
    path('filter-results-download', views.filter_results_download, name='filter-results-download'),

    
]