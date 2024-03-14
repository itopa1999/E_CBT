from django.urls import path, include
from .import views


urlpatterns = [
    path('login/', views.login_user, name='login_admin'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('changepassword', views.changepassword, name='changepassword'),
    
    path('decline', views.decline, name='decline'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    
    
    path('all-student', views.all_student, name='all-student'),
    path('edit-student/<int:pk>', views.edit_student, name='edit-student'),
    path('add-student', views.add_student, name='add-student'),
    path('del-all-student', views.del_all_student, name='del-all-student'),
    
    
    
    path('add-department', views.add_department, name='add-department'),
    path('department', views.department, name='department'),
    
    
    path('import-courses', views.import_courses, name='import-courses'),
    path('add-course', views.add_course, name='add-course'),
    path('course', views.course, name='course'),
    path('edit-course/<int:pk>', views.edit_course, name='edit-course'),
    
    
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
    
    
    
    path('submitmode', views.submitmode, name='submitmode'),
    path('exammode', views.exammode, name='exammode'),
    
    
    path('studentaccess', views.studentaccess, name='studentaccess'),
    path('examaccess', views.examaccess, name='examaccess'),
    path('levels', views.levels, name='levels'),
    path('add-level', views.add_level, name='add-level'),
    
    
    path('startexam/<int:pk>', views.startexam, name='startexam'),
    path('unstartexam/<int:pk>', views.unstartexam, name='unstartexam'),
    path('endexam/<int:pk>', views.endexam, name='endexam'),
    
    path('activate_student/<int:pk>', views.activate_student, name='activate_student'),
    path('deactivate_student/<int:pk>', views.deactivate_student, name='deactivate_student'),
    path('unendexam/<int:pk>', views.unendexam, name='unendexam'),
    
    path('exam_per_on', views.exam_per_on, name='exam_per_on'),
    path('exam_per_off', views.exam_per_off, name='exam_per_off'),
    path('exam_submit_on', views.exam_submit_on, name='exam_submit_on'),
    path('exam_submit_off', views.exam_submit_off, name='exam_submit_off'),
    path('student_permission_on', views.student_permission_on, name='student_permission_on'),
    path('student_permission_off', views.student_permission_off, name='student_permission_off'),
    path('view_result_on', views.view_result_on, name='view_result_on'),
    path('view_result_off', views.view_result_off, name='view_result_off'),
    path('stop_time_on', views.stop_time_on, name='stop_time_on'),
    path('stop_time_off', views.stop_time_off, name='stop_time_off'),
    
    
    path('filter-start-exam-on', views.filter_start_exam_on, name='filter-start-exam-on'),
    path('filter-start-exam-off', views.filter_start_exam_off, name='filter-start-exam-off'),
    path('filter-exam-submit-on', views.filter_exam_submit_on, name='filter-exam-submit-on'),
    path('filter-exam-submit-off', views.filter_exam_submit_off, name='filter-exam-submit-off'),
    
    path('t_c', views.tc, name='t_c'),
    
    path('filter-student-permission-on', views.filter_student_permission_on, name='filter-student-permission-on'),
    path('filter-student-permission-off', views.filter_student_permission_off, name='filter-student-permission-off'),

    path('e-pin-on', views.e_pin_on, name='e-pin-on'),
    path('e-pin-off', views.e_pin_off, name='e-pin-off'),
    path('e-pin', views.e_pin, name='e-pin'),
    
    path('generate-pins', views.generate_pins, name='generate-pins'),
    path('generate_unused_pin_pdf', views.generate_unused_pin_pdf, name='generate_unused_pin_pdf'),
    path('expire_pins', views.expire_pins, name='expire_pins'),
    
    path('edit-level', views.edit_level, name='edit-level'),
    path('edit_department', views.edit_department, name='edit_department'),
    path('actions', views.actions, name='actions'),
    path('expire_pins', views.expire_pins, name='expire_pins'),
    path('expire_pins', views.expire_pins, name='expire_pins'),
    path('expire_pins', views.expire_pins, name='expire_pins'),
    path('expire_pins', views.expire_pins, name='expire_pins'),

    
]