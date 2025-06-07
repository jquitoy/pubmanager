from django.urls import path
from . import views

urlpatterns = [
	path('', views.staff_list, name='staff_list'),
	
	path('staff/list/', views.staff_list, name='staff_list'),
	path('staff/add/', views.staff_add, name='staff_add'),
	path('staff/edit/<int:staffId>/', views.staff_edit, name='staff_edit'),
	path('staff/delete/<int:staffId>/', views.staff_delete, name='staff_delete'),



	path('roles/list', views.role_list, name='role_list'),
	path('roles/add', views.role_add, name='role_add'),
	path('roles/edit/<int:roleId>/', views.role_edit, name='role_edit'),
	path('roles/delete/<int:roleId>/', views.role_delete, name='role_delete'),



	path('task/add', views.task_add, name='task_add'),
	path('load_staffs/', views.load_staffs, name="load_staffs"),

	path('calendar/', views.calendar, name='calendar'),
	path('task/edit/<int:taskId>', views.task_edit, name='task_edit'),
	# path('task/delete/<int:taskId>', views.task_delete, name='task_delete'),	

	


]
