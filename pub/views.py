from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RoleForm, StaffForm
from .models import Roles, Staffs


# Create your views here.
def index(request):
    return render(request, 'users/usersList.html')

def staff_list(request):
    staffs = Staffs.objects.all()

    data = {
        'staffs': staffs
    }

    return render(request, 'staff/staffList.html', data)

def staff_add(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'staff/staffAdd.html', {'form': form})

def role_list(request):
    try:
        roles = Roles.objects.all()

        data = {
            'roles':roles
        }

        return render(request, 'staff/roleList.html', data)
    
    except Exception as e:
        return HttpResponse(f'Error occured during load Roles: {e}')


def role_add(request):
    try:
        if request.method == 'POST':
            role = request.POST.get('role')

            Roles.objects.create(role=role).save()
            return redirect('/roles/list')
        
        else:
            return render(request, 'staff/roleAdd.html')
        
    except Exception as e:
        return HttpResponse(f'Error occured during add gender: {e}')
    


def task_add(request):
    return render(request, 'task/taskAdd.html')