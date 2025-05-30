from django.urls import path
from . import views

urlpatterns = [
	path('index/', views.index, name='index'),
	path('staff/list/', views.staff_list, name='staff_list'),
	path('staff/add/', views.staff_add, name='staff_add'),


	path('roles/list', views.role_list, name='role_list'),
	path('roles/add', views.role_add, name='role_add'),


	path('task/add', views.task_add, name='task_add'),
	path('load_staffs/', views.load_staffs, name="load_staffs"),


]
