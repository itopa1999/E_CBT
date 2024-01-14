import django_filters
from django_filters import DateFilter
from .models import *
from users.models import User
from exam.models import Result


class StudentFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    userid = django_filters.CharFilter(field_name='userid', lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['first_name','last_name','userid','department']
        
        


class ResultFilter(django_filters.FilterSet):
    student__userid = django_filters.CharFilter(field_name='student__userid', lookup_expr='icontains')
    student__first_name = django_filters.CharFilter(field_name='student__first_name', lookup_expr='icontains')
    student__last_name = django_filters.CharFilter(field_name='student__last_name', lookup_expr='icontains')
    student__department = django_filters.CharFilter(field_name='student__department')
    marks__lte = django_filters.NumberFilter(field_name='marks', lookup_expr='lte')
    marks__gte = django_filters.NumberFilter(field_name='marks', lookup_expr='gte')
    class Meta:
        model = Result
        fields = ['student__userid','student__first_name','student__last_name','student__department','exam','marks__lte','marks__gte']