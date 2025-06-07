import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from .forms import RoleForm, StaffForm, TaskWithAssignmentForm
from .models import Roles, Staffs, Tasks, Assignments
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder


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
    staff = get_object_or_404(Staffs, pk=staffId)
    roles = Roles.objects.all()
    
    if request.method == "POST":
        # handle form submission
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
    
    if request.headers.get('HX-Request'):
        return render(request, "staff/partials/edit_form.html", {"staff": staff, "roles": roles})
    else:
        return render(request, "staff/staffEdit.html", {"staff": staff, "roles": roles})
    
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
            # Get counts for all roles in one query
        roles_with_counts = Roles.objects.annotate(
            staff_count=Count('staffs')  # Note the related_name
        ).order_by('role')


        data = {
            'roles':roles,
            'roles_with_counts': roles_with_counts,  # Add this line
        }

        if request.method == 'POST':
            role = request.POST.get('role_name')

            Roles.objects.create(role=role).save()
            return redirect('/roles/list')

        return render(request, 'staff/roleList.html', data)

    except Exception as e:
        return HttpResponse(f'Error occured during load Roles: {e}')


def role_add(request):
    try:
        if request.method == 'POST':
            role = request.POST.get('role_name')

            Roles.objects.create(role=role).save()
            return redirect('/roles/list')
        
        else:
            return render(request, 'staff/roleAdd.html')
        
    except Exception as e:
        return HttpResponse(f'Error occured during add gender: {e}')
    
def role_edit(request, roleId):
    try:
        roleObj = Roles.objects.get(pk=roleId)

        if request.method == 'POST':
            role = request.POST.get('role_name')
            roleObj.role = role
            roleObj.save()
            return redirect('/roles/list')

        else:
            data = {
                'role': roleObj,
            }
            if request.headers.get('HX-Request'):
                return render(request, 'staff/partials/edit_role_form.html', data)
            else:
                return render(request, 'staff/roleList.html', data)

    except Exception as e:
        return HttpResponse(f'Error occured during edit')
    

def role_delete(request, roleId):

    try:
        if request.method == 'POST':
            roleObj = Roles.objects.get(pk=roleId)
            roleObj.delete()

            return redirect('/roles/list')

        else:
            roleObj = Roles.objects.get(pk=roleId)

            data = {
                'role': roleObj,
            }

            return render(request, '/roles/list', data)


    
    except Exception as e:
        return HttpResponse(f'Error occured during delete gender: {e}')
    


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

def calendar(request):
    tasks = Tasks.objects.all()
    assignments = Assignments.objects.all()
    roles = Roles.objects.all()
    staffs = Staffs.objects.all()

    staff_by_role = {}
    for role in roles:
        staff_by_role[role.role_id] = [
            {'id': staff.staff_id, 'name': staff.full_name}
            for staff in staffs.filter(role=role)
        ]

    events = []
    for task in tasks:
        deadline = task.deadline
        event = {
            "id": task.id,
            "title": task.title,
            "start": deadline.strftime("%Y-%m-%d"),
            "description": task.description,
            "task_type": task.task_type,
            "status": task.status,
            "extendedProps": {
                "description": task.description,
                "task_type": task.task_type,
                "status": task.status,
                "assignments": [
                    {
                        "staff_id": assignment.staff.staff_id,
                        "role_id": int(assignment.role) if str(assignment.role).isdigit() else assignment.role,
                    }
                    for assignment in assignments.filter(task=task)
                ]
            }
        }
        events.append(event)

    data = {
        'tasks': tasks,
        'assignments': assignments,
        'roles': roles,
        'staff_by_role_json': json.dumps(staff_by_role, cls=DjangoJSONEncoder),
        'Tasks': Tasks,
        "events_json": json.dumps(events, cls=DjangoJSONEncoder),
    }

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        title = request.POST.get('title')
        task_type = request.POST.get('task_type')
        deadline = request.POST.get('deadline')
        description = request.POST.get('description')
        status = request.POST.get('status') or 'WORKING'
        roles_selected = request.POST.getlist('role[]')
        staffs_selected = request.POST.getlist('staff[]')
        if 'delete_task' in request.POST and task_id:
            # Delete task and its assignments
            Tasks.objects.filter(pk=task_id).delete()
            Assignments.objects.filter(task_id=task_id).delete()
            return redirect('/calendar')
        if task_id:
            # Edit existing task
            task = Tasks.objects.get(pk=task_id)
            task.title = title
            task.task_type = task_type
            task.deadline = deadline
            task.description = description
            task.status = status
            task.save()
            # Remove old assignments and add new
            Assignments.objects.filter(task=task).delete()
            for role_id, staff_id in zip(roles_selected, staffs_selected):
                if role_id and staff_id:
                    Assignments.objects.create(
                        task=task,
                        staff=Staffs.objects.get(pk=staff_id),
                        role=Roles.objects.get(pk=role_id).role_id
                    )
        else:
            # Add new task
            task = Tasks.objects.create(
                title=title,
                task_type=task_type,
                deadline=deadline,
                description=description,
                status=status,
            )
            for role_id, staff_id in zip(roles_selected, staffs_selected):
                if role_id and staff_id:
                    Assignments.objects.create(
                        task=task,
                        staff=Staffs.objects.get(pk=staff_id),
                        role=Roles.objects.get(pk=role_id).role_id
                    )
        return redirect('/calendar')

    return render(request, 'task/calendar.html', data)

def task_edit(request, taskId):
    task = get_object_or_404(Tasks, pk=taskId)
    assignments = Assignments.objects.filter(task=task)

    if request.method == "POST":
        # handle form submission
        title = request.POST.get('title')
        task_type = request.POST.get('task_type')
        deadline = request.POST.get('deadline')
        description = request.POST.get('description')

        task.title = title
        task.task_type = task_type
        task.deadline = deadline
        task.description = description
        task.save()

        return redirect('/calendar')

    return render(request, 'task/taskEdit.html', {'task': task, 'assignments': assignments})