import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from .forms import RoleForm, StaffForm, TaskWithAssignmentForm
from .models import Roles, Staffs, Tasks, Assignments
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def login_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Django's default User uses username, not email, so we must look up the username
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            username = None
        if username:
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('calendar')
            else:
                error = 'Invalid credentials or not a superuser.'
        else:
            error = 'Invalid credentials or not a superuser.'
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def staff_list(request):
    staffs = Staffs.objects.all().order_by('staff_id')
    roles = Roles.objects.all()

    # Pagination logic
    page_number = request.GET.get('page', 1)
    paginator = Paginator(staffs, 5)  # 10 staff per page
    page_obj = paginator.get_page(page_number)
    staffCount = Staffs.objects.all().count()

    data = {
        'staffCount': staffCount,
        'staffs': page_obj.object_list,
        'roles': roles,
        'page_obj': page_obj,
        'paginator': paginator,
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
        staff.role.set(roles_selected)
        staff.save()

        # Re-paginate after adding
        staffs = Staffs.objects.all().order_by('staff_id')
        paginator = Paginator(staffs, 5)
        page_obj = paginator.get_page(1)
        data['staffs'] = page_obj.object_list
        data['page_obj'] = page_obj
        data['paginator'] = paginator

        return render(request, 'staff/staffList.html', data)

    return render(request, 'staff/staffList.html', data)

@login_required
def staff_add(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'staff/staffAdd.html', {'form': form})

@login_required
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
    
@login_required
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

@login_required
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


@login_required
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
    
@login_required
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
    

@login_required
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
    


@login_required
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

@login_required
def load_staffs(request):
    role_id = request.GET.get('role')
    staffs = Staffs.objects.filter(role=role_id)
    return render(request, 'staff/staffOptions.html', {'staffs': staffs})


@login_required
def get_staff_form(request, staff_id):
    staff = get_object_or_404(Staffs, id=staff_id)
    return render(request, 'staff/staffList.html', {'staff': staff})

@login_required
def calendar(request):
    tasks = Tasks.objects.all()
    assignments = Assignments.objects.all()
    roles = Roles.objects.all()
    staffs = Staffs.objects.all()
    tasksPending = Tasks.objects.filter(status='PENDING').order_by('deadline')

    taskPostedCount = Tasks.objects.filter(status='POSTED').count()
    taskPendingCount = Tasks.objects.filter(status='PENDING').count()
    taskMissedCount = Tasks.objects.filter(status='MISSED').count()


    staff_by_role = {}
    for role in roles:
        staff_by_role[role.role_id] = [
            {'id': staff.staff_id, 'name': staff.full_name, 'email': staff.email}
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
                "google_event_id": task.google_event_id,
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

    # Compute abbreviated staff names for each task
    from collections import defaultdict
    tasksPending = Tasks.objects.filter(status='PENDING').order_by('deadline')
    tasks_pending_with_staff = []
    for task in tasksPending:
        # Get all assignments for this task, sorted by staff full name
        assignments = list(Assignments.objects.filter(task=task).select_related('staff').order_by('staff__full_name'))
        # Build a map of last_name -> list of (first_name, full_name)
        last_name_map = defaultdict(list)
        for a in assignments:
            parts = a.staff.full_name.strip().split()
            if len(parts) == 1:
                first_name, last_name = parts[0], ''
            else:
                first_name, last_name = parts[0], parts[-1]
            last_name_map[last_name].append((first_name, a.staff.full_name))
        # Now, for each assignment, compute the display name
        staff_display = []
        for a in assignments:
            parts = a.staff.full_name.strip().split()
            if len(parts) == 1:
                first_name, last_name = parts[0], ''
            else:
                first_name, last_name = parts[0], parts[-1]
            same_last = sorted(last_name_map[last_name])
            # Find this staff's index among those with the same last name
            idx = [fn for fn, full in same_last].index(first_name)
            if len(same_last) > 1 and idx > 0:
                abbr = f"{first_name[:2]}.{last_name}"
            else:
                abbr = f"{first_name[:1]}.{last_name}"
            staff_display.append(abbr)
        tasks_pending_with_staff.append({
            'task': task,
            'staff_display': staff_display,
        })

    data = {
        'tasks': tasks,
        'assignments': assignments,
        'roles': roles,
        'staff_by_role_json': json.dumps(staff_by_role, cls=DjangoJSONEncoder),
        "events_json": json.dumps(events, cls=DjangoJSONEncoder),
        "Tasks": Tasks,
        "tasksPending": tasksPending,
        "tasksPendingWithStaff": tasks_pending_with_staff,
        "taskPostedCount": taskPostedCount,
        "taskPendingCount": taskPendingCount,
        "taskMissedCount": taskMissedCount,
    }

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        title = request.POST.get('title')
        task_type = request.POST.get('task_type')
        deadline = request.POST.get('deadline')
        description = request.POST.get('description')
        status = request.POST.get('status') or 'PENDING'
        roles_selected = request.POST.getlist('role[]')
        staffs_selected = request.POST.getlist('staff[]')
        google_event_id = request.POST.get('google_event_id')
        print('should delete after')
        if request.POST.get('action') == 'delete' and task_id:
            try:
                task_id_int = int(task_id)
            except ValueError:
                print("task_id is not an integer:", task_id)
                return redirect('/calendar')
            print("Attempting to delete task with id:", task_id_int)
            print("Tasks matching:", Tasks.objects.filter(pk=task_id_int))
            Tasks.objects.filter(pk=task_id_int).delete()
            Assignments.objects.filter(task_id=task_id_int).delete()
            return redirect('/calendar')
        if task_id:
            # Edit existing task
            task = Tasks.objects.get(pk=task_id)
            task.title = title
            task.task_type = task_type
            task.deadline = deadline
            task.description = description
            task.status = status
            if google_event_id:
                task.google_event_id = google_event_id
            else:
                # If not present, clear it
                task.google_event_id = None
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
                google_event_id=google_event_id
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

@login_required
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

# def report(request):
#     tasks = Tasks.objects.all()
#     assignments = Assignments.objects.all()
#     roles = Roles.objects.all()
#     staffs = Staffs.objects.all()

#     taskPostedCount = Tasks.objects.filter(status='POSTED').count()
#     taskPendingCount = Tasks.objects.filter(status='PENDING').count()
#     taskMissedCount = Tasks.objects.filter(status='MISSED').count()

#     data = {
#         'tasks': tasks,
#         'assignments': assignments,
#         'roles': roles,
#         'staffs': staffs,
#         "taskPostedCount": taskPostedCount,
#         "taskPendingCount": taskPendingCount,
#         "taskMissedCount": taskMissedCount,
#     }

#     return render(request, 'dashboard/dashboard.html', data)

@login_required
def dashboard(request):
    staffs = Staffs.objects.all().order_by('staff_id')
    staff_names = [s.full_name for s in staffs]
    pendingTotal = Tasks.objects.filter(status='PENDING').count()

    taskPostedCount = Tasks.objects.filter(status='POSTED').count()
    taskPendingCount = Tasks.objects.filter(status='PENDING').count()
    taskMissedCount = Tasks.objects.filter(status='MISSED').count()
    taskTotal = Tasks.objects.exclude(status='CANCELLED').count()

    # For each staff, count tasks by status
    posted_counts = []
    pending_counts = []
    missed_counts = []
    for staff in staffs:
        assignments = Assignments.objects.filter(staff=staff)
        posted = assignments.filter(task__status='POSTED').count()
        pending = assignments.filter(task__status='PENDING').count()
        missed = assignments.filter(task__status='MISSED').count()
        posted_counts.append(posted)
        pending_counts.append(pending)
        missed_counts.append(missed)

    # Role breakdown for pie chart
    roles = Roles.objects.all()
    role_labels = [role.role for role in roles]
    # Count assignments per role (Assignments.role stores role_id as string/int)
    role_counts = [Assignments.objects.filter(role=str(role.role_id)).count() for role in roles]

    data = {
        "staffs": staffs,
        'staff_names': json.dumps(staff_names),
        'posted_counts': json.dumps(posted_counts),
        'pending_counts': json.dumps(pending_counts),
        'missed_counts': json.dumps(missed_counts),
        'role_labels': json.dumps(role_labels),
        'role_counts': json.dumps(role_counts),
        'staffNames': staff_names,
        'postedCounts': posted_counts,
        'pendingCounts': pending_counts,    
        'missedCounts': missed_counts,
        'pendingTotal': pendingTotal,
        # New context for tasks progress bar
        'tasks_posted': taskPostedCount,
        'tasks_pending': taskPendingCount,
        'tasks_missed': taskMissedCount,
        'tasks_total': taskTotal,

    }
    return render(request, 'dashboard/dashboard.html', data)