from django import forms
from .models import Staffs, Roles, Tasks, Assignments

class RoleForm(forms.Form):
    name = forms.CharField(label="Role Name", max_length=100)

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staffs
        fields = ['full_name', 'position', 'email', 'role', 'google_calendar_id']
        widgets = {
            'role': forms.CheckboxSelectMultiple,  # Because it's a ManyToManyField
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = Roles.objects.all()
        self.fields['role'].label_from_instance = lambda obj: obj.role  # Display the 'role' field of Roles model


class TaskWithAssignmentForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
        }),
        label="Deadline Date"
    )

    role = forms.ModelChoiceField(
        queryset=Roles.objects.all(),
        label="Select Role",
        widget=forms.Select(attrs={
            'class': 'role-select',
            'id': 'id_role',
            'hx-get': '/load_staffs/',  # Ensure this URL is correct and starts with a slash
            'hx-target': '#id_staff',
        })
    )

    staff = forms.ModelChoiceField(
        queryset=Staffs.objects.none(),  # Will be set in __init__
        label="Select Staff",
        widget=forms.Select(attrs={
            'class': 'staff-dropdown',
            'id': 'id_staff',

        })
    )

    class Meta: 
        model = Tasks
        fields = ['title', 'task_type', 'deadline', 'description', 'role']

    def __init__(self, *args, **kwargs):
        # if 'data' in kwargs:
        #     role_id = kwargs['data'].get('role') or kwargs['data'].get('id_role')
        super().__init__(*args, **kwargs)
        self.fields['role'].label_from_instance = lambda obj: obj.role

        if "role" in self.data:
            role_id = int(self.data.get("role"))
            self.fields['staff'].queryset = Staffs.objects.filter(role=role_id)

        # if role_id:
        #     self.fields['staff'].queryset = Staffs.objects.filter(role=role_id)
        # else:
        #     self.fields['staff'].queryset = Staffs.objects.none()