
from django import forms
from .models import *
from django import forms
from django.contrib.auth.models import User
from .models import Projects
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'first_name', 'last_name', 'birthdaydate', 'email',
            'phone', 'gender', 'department', 'position', 'hire_date',
            'status', 'Educations', 'Address', 'Country', 'Company'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthdaydate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'Educations': forms.Select(attrs={'class': 'form-select'}),
            'Address': forms.TextInput(attrs={'class': 'form-control'}),
            'Country': forms.TextInput(attrs={'class': 'form-control'}),
            'Company': forms.TextInput(attrs={'class': 'form-control'}),
        }




class MySkillForm(forms.ModelForm):
    class Meta:
        model = MySkill
        fields = ['skill', 'date', 'percentage']


class NotificationForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_staff=False),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Select Specific Employees"
    )

    send_to_all = forms.BooleanField(
        required=False,
        label="Send to All Employees",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Notifications
        fields = ['category', 'message', 'send_to_all', 'recipients']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
# JOb Form
class job(forms.Form):
    class Meta:
        models = 'Job'
        fields = '__all__'


class AssignProjectForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Assign To",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = Projects
        fields = ['user', 'name', 'team', 'hour', 'deadline', 'priority']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Project Name'}),
            'team': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team Name'}),
            'hour': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Estimated Hours'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            # ✅ FIXED: Use DateInput instead of DateField
            'deadline': forms.DateInput(
                attrs={
                    'class': 'form-control datepicker',
                    'placeholder': 'Select deadline',
                    'autocomplete': 'off'
                }
            ),
        }



class TaskForm(forms.ModelForm):

    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_staff=False),
        required=False,
        widget=forms.CheckboxSelectMultiple,  
        label="Assign to specific employees")
    assign_to_all = forms.BooleanField(required=False, label="Assign to all employees")

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assign_to_all', 'assigned_to']


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-control rounded-3 shadow-sm'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-control rounded-3 shadow-sm'
            }),
            'reason': forms.Textarea(attrs={
                'rows': 3, 'class': 'form-control rounded-3 shadow-sm',
                'placeholder': 'Enter reason for leave...'
            }),
        }



class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['employee', 'basic_salary', 'hra', 'deductions', 'month', 'year']



class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'is_public']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }