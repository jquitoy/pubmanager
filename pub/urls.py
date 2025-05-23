from django.urls import path
from . import views

urlpatterns = [
	path('index/', views.index, name='index'),
	path('staff/list/', views.staff_list, name='staff_list'),
	
]
