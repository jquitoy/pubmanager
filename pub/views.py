import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from .forms import RoleForm, StaffForm, TaskWithAssignmentForm
from .models import Roles, Staffs, Tasks, Assignments


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


# def task_add(request):
#     roles = Roles.objects.all()


#     data = {
#         'roles':roles,

#     }

#     return render(request, 'task/taskAdds.html', data)



def form_valid(self, form):
    task = form.save(commit=False)
    task.created_by = self.request.user
    task.save()
    
    # Process selected staff
    try:
        selected_staff = json.loads(form.cleaned_data['selected_staff'] or '[]')
        for staff_data in selected_staff:
            Assignments.objects.create(
                task=task,
                staff_id=staff_data['id'],
                role=form.cleaned_data['role'],
                status='ACCEPTED' if task.task_type == Tasks.OBSERVANCE else 'PENDING'
            )
    except json.JSONDecodeError:
        pass
    
    return super().form_valid(form)
