from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from django.forms import ModelForm
from .models import Resident, Medication, Employee, EmploymentStatus, \
     MedicalSupply, MedicalEquipment, Charge, ResidentWeight, Drug
from django.contrib.auth.models import User
from simple_search import search_form_factory

SearchForm = search_form_factory(Resident.objects.all(), ['first_name', 'last_name'])

DrugSearchForm = search_form_factory(Drug.objects.all(), ['generic_name', 'brand_name'])

class DateInput(forms.DateInput):
    input_type = 'date'
    
class TimeInput(forms.TimeInput):
    input_type = 'time'

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class ChargeCreateForm(ModelForm):
    class Meta:
        model = Charge
        fields = '__all__'
        widgets = {
            'date_acquired': DateInput(),            
            }

class MedicationCreateForm(ModelForm):
    class Meta:
        model = Medication
        fields = '__all__'
        widgets = {
            'date_started': DateInput(),
            'due': DateInput(),            
            }
        
class ResidentCreateForm(ModelForm):
    class Meta:
        model = Resident
        fields = '__all__'
        widgets = {
                    'birth_date': DateInput(),
                    'admission_date': DateInput(),
                    'admission_time': TimeInput(),                    
                    #'physicians': forms.CheckboxSelectMultiple(),
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

class MedicalSupplyCreateForm(ModelForm):
    class Meta:
        model = MedicalSupply
        exclude = ('id',)
        widgets = {
                'date_acquired': DateInput(),
                'expiration_date': DateInput(),
            }

class MedicalEquipmentCreateForm(ModelForm):
    class Meta:
        model = MedicalEquipment
        exclude = ('id',)
        widgets = {
                'date_acquired': DateInput(),
                'due_back': DateInput(),
            }

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        exclude = ('password', 'last_login',
                'is_superuser', 'groups',
                'user_permissions', 'is_staff',
                'is_active', 'date_joined',)

class ResidentWeightCreateForm(ModelForm):
    class Meta:
        model = ResidentWeight
        fields = '__all__'
        widgets = {'date': DateInput(),}



