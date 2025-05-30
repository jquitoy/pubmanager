import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from .forms import RoleForm, StaffForm, TaskWithAssignmentForm
from .models import Roles, Staffs, Tasks, Assignments


# Create your views here.
def index(request):
    return render(request, 'users/usersList.html')

def staff_list(request):
    staffs = Staffs.objects.all()
    roles = Roles.objects.all()

    data = {
        'staffs': staffs,
        'roles': roles,  # Add this line
    }

    if request.method == 'POST':
        fullName = request.POST.get('full_name')
        position = request.POST.get('position')
        email = request.POST.get('email')
        roles_selected = request.POST.getlist('role[]')

        staff = Staffs.objects.create(
            full_name = fullName,
            position = position,
            email = email,
        )
        # Assuming Staffs has a ManyToManyField to Roles named 'role'
        staff.role.set(roles_selected)
        staff.save()

        return render(request, 'staff/staffList.html', data)


        

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

def staff_edit(request, staffId):
    try:
        if request.method == 'POST':
            staffObj = Staffs.objects.get(pk=staffId)

            fullName = request.POST.get('full_name')
            position = request.POST.get('position')
            email = request.POST.get('email')
            roles_selected = request.POST.getlist('role[]')

            form_data = {
                'fullName': fullName,
                'position': position,
                'email': email,
                'roles_selected': roles_selected
            }

            # Update staff if validation passes
            staffObj.full_name = fullName
            staffObj.position = position
            staffObj.email = email
            staffObj.role.set(roles_selected)
            staffObj.save()

            return redirect('/staff/list')

        else:
            staffObj = Staffs.objects.get(pk=staffId)
            roles = Roles.objects.all()

            data = {
                'staff': staffObj,
                'roles': roles
            }

            return render(request, 'staff/staffEdit.html', data)

    except Exception as e:
        return HttpResponse(f'Error occured during edit staff: {e}')
    
def staff_delete(request, staffId):

    try:
        if request.method == 'POST':
            staffObj = Staffs.objects.get(pk=staffId)
            staffObj.delete()

            return redirect('/staff/list')

        else:
            staffObj = Staffs.objects.get(pk=staffId)
            roles = Roles.objects.all()

            data = {
                'staff': staffObj,
                'roles': roles
            }

            return render(request, 'staff/deleteStaff.html', data)


    
    except Exception as e:
        return HttpResponse(f'Error occured during delete gender: {e}')

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
    if request.method == 'POST':
        form = TaskWithAssignmentForm(request.POST)
        # Only validate if the submit button was pressed
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            staff_member = form.cleaned_data['staff']
            role = form.cleaned_data['role']
            Assignments.objects.create(
                task=task,
                staff=staff_member,
                role=role.role_id
            )
            return redirect('task_add')
        # If not a real submission, just render the form with filtered staff
    else:
        form = TaskWithAssignmentForm()
    return render(request, 'task/taskAdd.html', {'form': form})

def load_staffs(request):
    role_id = request.GET.get('role')
    staffs = Staffs.objects.filter(role=role_id)
    return render(request, 'staff/staffOptions.html', {'staffs': staffs})


def get_staff_form(request, staff_id):
    staff = get_object_or_404(Staffs, id=staff_id)
    return render(request, 'staff/staffList.html', {'staff': staff})