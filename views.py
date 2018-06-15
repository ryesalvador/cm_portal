from django.shortcuts import render
from .models import Resident, Physician, Relative, \
     PerformanceAppraisal, EmploymentStatus, Employee, Position, Department
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

@login_required
def index(request):    
    return render(request, 'cm_portal/index.html')

@login_required
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

@login_required
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

class ResidentCreate(LoginRequiredMixin, generic.CreateView):
    model = Resident
    fields = '__all__'

class ResidentUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Resident
    fields = '__all__'
    template_name_suffix = '_update_form'

class ResidentDelete(LoginRequiredMixin, generic.DeleteView):
    model = Resident
    success_url = reverse_lazy('residents')
    
class PhysicianListView(LoginRequiredMixin, generic.ListView):
    model = Physician

class PhysicianDetailView(LoginRequiredMixin, generic.DetailView):
    model = Physician

class PhysicianCreate(LoginRequiredMixin, generic.CreateView):
    model = Physician
    fields = '__all__'

class PhysicianUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Physician
    fields = '__all__'
    template_name_suffix = '_update_form'

class PhysicianDelete(LoginRequiredMixin, generic.DeleteView):
    model = Physician
    success_url = reverse_lazy('physicians')
    
class RelativeListView(LoginRequiredMixin, generic.ListView):
    model = Relative    

class RelativeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Relative

class RelativeCreate(LoginRequiredMixin, generic.CreateView):
    model = Relative
    fields = '__all__'

class RelativeUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Relative
    fields = '__all__'
    template_name_suffix = '_update_form'

class RelativeDelete(LoginRequiredMixin, generic.DeleteView):
    model = Relative
    success_url = reverse_lazy('relatives')
    
class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee

class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee

class EmployeeCreate(LoginRequiredMixin, generic.CreateView):
    model = Employee
    fields = '__all__'

class EmployeeUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Employee
    fields = '__all__'
    template_name_suffix = '_update_form'

class EmployeeDelete(LoginRequiredMixin, generic.DeleteView):
    model = Employee
    success_url = reverse_lazy('employees')

class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position

class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position

class DepartmentListView(LoginRequiredMixin, generic.ListView):
    model = Department

class DepartmentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Department
