from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.get_students, name='get_students'),
    path('students/filter/', views.filter_students, name='filter_students'),
]
