from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from django.forms import ModelForm
from .models import Resident, Employee, EmploymentStatus
from datetimewidget.widgets import DateWidget, DateTimeWidget

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class ResidentCreateForm(ModelForm):
    class Meta:
        model = Resident
        exclude = ['photo',]
        widgets = {
                    'birth_date': DateWidget(),
                    'date_and_time_of_admission': DateTimeWidget(),
                    'died_on': DateTimeWidget(),
                    'discharged_on': DateWidget(),
                }

class EmployeeCreateForm(ModelForm):
    class Meta:
        model = Employee
        exclude = ['photo',]
        widgets = {
                    'birth_date': DateWidget(),
                }

class EmploymentStatusCreateForm(ModelForm):
    class Meta:
        model = EmploymentStatus
        fields = '__all__'
        widgets = {
                    'date_started': DateWidget(),
                    'date_due': DateWidget(),
                }
