from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from django.forms import ModelForm
from .models import Resident, Employee, EmploymentStatus
from datetimewidget.widgets import DateWidget, DateTimeWidget

dateOptions = {
        'format': 'mm/dd/yyyy'
    }

dateTimeOptions = {
        'format': 'mm/dd/yyyy hh:ii' 
    }

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class ResidentCreateForm(ModelForm):
    class Meta:
        model = Resident
        fields = '__all__'
        widgets = {
                    'birth_date': DateWidget(options=dateOptions),
                    'date_and_time_of_admission': DateTimeWidget(options=dateTimeOptions),
                    'died_on': DateTimeWidget(options=dateTimeOptions),
                    'discharged_on': DateWidget(options=dateOptions),
                }

class EmployeeCreateForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
                    'birth_date': DateWidget(options=dateOptions),
                }

class EmploymentStatusCreateForm(ModelForm):
    class Meta:
        model = EmploymentStatus
        fields = '__all__'
        widgets = {
                    'date_started': DateWidget(options=dateOptions),
                    'date_due': DateWidget(options=dateOptions),
                }

class SearchForm(forms.Form):
    query = forms.CharField(            
            widget=forms.TextInput({'size': 32}))



