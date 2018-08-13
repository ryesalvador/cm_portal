from django.shortcuts import render
from .models import Resident, Physician, Relative, Relationship, \
     PerformanceAppraisal, EmploymentStatus, Employee, Position, Department
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import ResidentCreateForm, EmployeeCreateForm, SearchForm
from django.http import HttpResponseRedirect
from itertools import chain
from django.apps import apps
from django import forms
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

@login_required
def search(request, model, template_name):
    form = SearchForm()
    form.fields['query'].widget = forms.TextInput(
        attrs={
            'placeholder': 'Search {}s...'.format(model),
            'size': 32
            })
    obj_list = []
    show_results = False
    if 'query' in request.GET:
        show_results = True
        query = request.GET['query'].strip()
        if query:
            form = SearchForm({'query': query})            
            cls = apps.get_model('cm_portal', model)
            query0 = cls.objects.filter(last_name__icontains=query)
            query1 = cls.objects.filter(first_name__icontains=query)
            obj_list = list(chain(query0, query1))            
    variables = {
            'form': form,
            'obj_list': obj_list,
            'show_results': show_results,
            }
    return render(request, 'cm_portal/{}'.format(template_name), variables)
    

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
                      'num_relatives': num_relatives,                      
                      })

@login_required
def hris_index(request):
    num_employees = Employee.objects.all().count()
    return render(request,
                  'cm_portal/hris_index.html',
                  context={
                      'num_employees': num_employees
                      })

@method_decorator(cache_control(private=True), name='dispatch')
class ResidentListView(LoginRequiredMixin, generic.ListView):
    model = Resident
    paginate_by = 10    
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ResidentListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context        
        form = SearchForm()
        form.fields['query'].widget = forms.TextInput(
        attrs={
            'placeholder': 'Search Residents...',
            'size': 32
            })
        context['form'] = form        
        return context

@method_decorator(cache_control(private=True), name='dispatch')
class ResidentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Resident

class ResidentCreate(LoginRequiredMixin, generic.CreateView):
    model = Resident
    form_class = ResidentCreateForm

class ResidentUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Resident
    form_class = ResidentCreateForm
    template_name_suffix = '_update_form'

class ResidentDelete(LoginRequiredMixin, generic.DeleteView):
    model = Resident
    success_url = reverse_lazy('residents')
    
class PhysicianListView(LoginRequiredMixin, generic.ListView):
    model = Physician
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PhysicianListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context        
        form = SearchForm()
        form.fields['query'].widget = forms.TextInput(
        attrs={
            'placeholder': 'Search Physicians...',
            'size': 32
            })
        context['form'] = form        
        return context

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
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(RelativeListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context        
        form = SearchForm()
        form.fields['query'].widget = forms.TextInput(
        attrs={
            'placeholder': 'Search Relatives...',
            'size': 32
            })
        context['form'] = form        
        return context

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
   
class RelationshipListView(LoginRequiredMixin, generic.ListView):
    model = Relationship
    paginate_by = 10

class RelationshipDetailView(LoginRequiredMixin, generic.DetailView):
    model = Relationship

class RelationshipCreate(LoginRequiredMixin, generic.CreateView):
    model = Relationship
    fields = '__all__'

class RelationshipUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Relationship
    fields = '__all__'
    template_name_suffix = '_update_form'

class RelationshipDelete(LoginRequiredMixin, generic.DeleteView):
    model = Relationship
    success_url = reverse_lazy('relationship')

class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context        
        form = SearchForm()
        form.fields['query'].widget = forms.TextInput(
        attrs={
            'placeholder': 'Search Employees...',
            'size': 32
            })
        context['form'] = form        
        return context

class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee

class EmployeeCreate(LoginRequiredMixin, generic.CreateView):
    model = Employee
    form_class = EmployeeCreateForm

class EmployeeUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Employee
    fields = '__all__'
    template_name_suffix = '_update_form'

class EmployeeDelete(LoginRequiredMixin, generic.DeleteView):
    model = Employee
    success_url = reverse_lazy('employees')

class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 10

class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position

class PositionCreate(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = '__all__'

class PositionUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = '__all__'
    template_name_suffix = '_update_form'

class PositionDelete(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy('positions')

class DepartmentListView(LoginRequiredMixin, generic.ListView):
    model = Department
    paginate_by = 10

class DepartmentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Department

class DepartmentCreate(LoginRequiredMixin, generic.CreateView):
    model = Department
    fields = '__all__'

class DepartmentUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Department
    fields = '__all__'
    template_name_suffix = '_update_form'

class DepartmentDelete(LoginRequiredMixin, generic.DeleteView):
    model = Department
    success_url = reverse_lazy('departments')

