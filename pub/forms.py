from django import forms
from .models import Staffs, Roles

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

