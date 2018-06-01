from django.shortcuts import render
from .models import Resident, Physician, Relative, \
     PerformanceAppraisal, EmploymentStatus, Employee, Position, Department
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.mixins import PermissionRequiredMixin

def index(request):    
    return render(request, 'cm_portal/index.html')

def nursing_home_index(request):
    num_residents = Resident.objects.all().count()
    num_physicians = Physician.objects.all().count()
    num_relatives = Relative.objects.all().count()
    
    return render(request,
                  'cm_portal/nursing_home_index.html',
                  context={
                      'num_residents': num_residents,
                      'num_physicians': num_physicians,
                      'num_relatives': num_relatives
                      })

def hris_index(request):
    num_employees = Employee.objects.all().count()
    return render(request,
                  'cm_portal/hris_index.html',
                  context={
                      'num_employees': num_employees
                      })

class ResidentListView(LoginRequiredMixin, generic.ListView):
    model = Resident

class ResidentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Resident

class PhysicianListView(LoginRequiredMixin, generic.ListView):
    model = Physician

class PhysicianDetailView(LoginRequiredMixin, generic.DetailView):
    model = Physician

class RelativeListView(LoginRequiredMixin, generic.ListView):
    model = Relative    

class RelativeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Relative

class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee

class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee
