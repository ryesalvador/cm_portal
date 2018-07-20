from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from django.forms import ModelForm
from .models import Resident, Employee, EmploymentStatus

class DateInput(forms.DateInput):
    input_type = 'date'
    
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

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
                    'birth_date': DateInput(),
                    'date_and_time_of_admission': DateTimeInput(),
                    'died_on': DateInput(),
                    'discharged_on': DateInput(),
                }

class EmployeeCreateForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
                    'birth_date': DateInput(),
                }

class EmploymentStatusCreateForm(ModelForm):
    class Meta:
        model = EmploymentStatus
        fields = '__all__'
        widgets = {
                    'date_started': DateInput(),
                    'date_due': DateInput(),
                }

class SearchForm(forms.Form):
    query = forms.CharField(            
            widget=forms.TextInput({'size': 32}))



