from import_export import resources, fields
from users.models import User
from .models import Question, Course, Theory_Question

class UserFile(resources.ModelResource):
    class Meta:
        model = User
    
        
        
class QuestionFile(resources.ModelResource):
    class Meta:
        model = Question
        


class TheoryQuestionFile(resources.ModelResource):
    class Meta:
        model = Theory_Question
        fields = ['id','question','teacher_answer','marks']
 
        
class CourseFile(resources.ModelResource):
    class Meta:
        model = Course