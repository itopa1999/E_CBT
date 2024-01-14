from import_export import resources, fields
from users.models import User
from .models import Question, Course

class UserFile(resources.ModelResource):
    class Meta:
        model = User
    
        
        
class QuestionFile(resources.ModelResource):
    class Meta:
        model = Question
        
        
        
class CourseFile(resources.ModelResource):
    class Meta:
        model = Course