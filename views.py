from django.shortcuts import render
from .models import Resident, Physician, Relative, Relationship, \
     PerformanceAppraisal, EmploymentStatus, Employee, Position, Department, \
     MedicalAbstract, Drug, Medication, Item, ItemInstance
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ResidentCreateForm, EmployeeCreateForm, SearchForm, \
     MedicationCreateForm
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
            if model == 'Drug':
                query0 = cls.objects.filter(generic_name__icontains=query)
                query1 = cls.objects.filter(brand_name__icontains=query)
            else:
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
    num_residents = Resident.objects.filter(vital_status='LI').count()
    num_physicians = Physician.objects.all().count()
    num_relatives = Relative.objects.all().count()
    census_rebuschini = Resident.objects.filter(vital_status='LI').filter(building='R').count()
    census_luigi = Resident.objects.filter(vital_status='LI').filter(building='L').count()
    census_first_floor = Resident.objects.filter(vital_status='LI').filter(building='1').count()
    census_second_floor = Resident.objects.filter(vital_status='LI').filter(building='2').count()
    
    return render(request,
                  'cm_portal/nursing_home_index.html',
                  context={
                      'num_residents': num_residents,
                      'num_physicians': num_physicians,
                      'num_relatives': num_relatives,
                      'census_rebuschini': census_rebuschini,
                      'census_luigi': census_luigi,
                      'census_first_floor': census_first_floor,
                      'census_second_floor': census_second_floor,
                      })

@login_required
def hris_index(request):
    num_employees = Employee.objects.all().count()
    return render(request,
                  'cm_portal/hris_index.html',
                  context={
                      'num_employees': num_employees
                      })

@login_required
def inventory_index(request):
    num_items = Item.objects.all().count()
    num_actual_items = ItemInstance.objects.all().count()
    return render(request,
                  'cm_portal/inventory_index.html',
                  context={
                      'num_items': num_items,
                      'num_actual_items': num_actual_items
                      })

@login_required
def maintenance(request):
    male_first_floor = Resident.objects.filter(building='1').filter(gender='M')
    female_first_floor = Resident.objects.filter(building='1').filter(gender='F')
    male_second_floor = Resident.objects.filter(building='2').filter(gender='M')
    female_second_floor = Resident.objects.filter(building='2').filter(gender='F')
    male_luigi_tezza = Resident.objects.filter(building='L').filter(gender='M')
    female_luigi_tezza = Resident.objects.filter(building='L').filter(gender='F')
    male_rebuschini = Resident.objects.filter(building='R').filter(gender='M')
    female_rebuschini = Resident.objects.filter(building='R').filter(gender='F')
    return render(request,
                  'cm_portal/maintenance.html',
                  context={
                      'male_first_floor': male_first_floor,
                      'female_first_floor': female_first_floor,
                      'male_second_floor': male_second_floor,
                      'female_second_floor': female_second_floor,
                      'male_luigi_tezza': male_luigi_tezza,
                      'female_luigi_tezza': female_luigi_tezza,
                      'male_rebuschini': male_rebuschini,
                      'female_rebuschini': female_rebuschini,
                      })
    
@method_decorator(cache_control(private=True), name='dispatch')
class ResidentListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Resident
    queryset = Resident.objects.filter(vital_status='LI')
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
class DeceasedListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Resident
    queryset = Resident.objects.filter(vital_status='DE')
    template_name = 'cm_portal/resident_list_deceased.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(DeceasedListView, self).get_context_data(**kwargs)
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
class DischargedListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Resident
    queryset = Resident.objects.filter(vital_status='DC')
    template_name = 'cm_portal/resident_list_discharged.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(DischargedListView, self).get_context_data(**kwargs)
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
class ResidentDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Resident

class ResidentCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_resident'
    model = Resident
    form_class = ResidentCreateForm

class ResidentUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_resident'
    model = Resident
    form_class = ResidentCreateForm
    template_name_suffix = '_update_form'

class ResidentDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_resident'
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

class PhysicianCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_physician'
    model = Physician
    fields = '__all__'

class PhysicianUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_physician'
    model = Physician
    fields = '__all__'
    template_name_suffix = '_update_form'

class PhysicianDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_physician'
    model = Physician
    success_url = reverse_lazy('physicians')
    
class RelativeListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
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

class RelativeDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Relative

class RelativeCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_relative'
    model = Relative
    fields = '__all__'

class RelativeUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_relative'
    model = Relative
    fields = '__all__'
    template_name_suffix = '_update_form'

class RelativeDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_relative'
    model = Relative
    success_url = reverse_lazy('relatives')
   
class RelationshipListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Relationship
    paginate_by = 10

class RelationshipDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Relationship

class RelationshipCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_relationship'
    model = Relationship
    fields = '__all__'

class RelationshipUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_relationship'
    model = Relationship
    fields = '__all__'
    template_name_suffix = '_update_form'

class RelationshipDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_relationship'
    model = Relationship
    success_url = reverse_lazy('relationship')

@method_decorator(cache_control(private=True), name='dispatch')
class EmployeeListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_hris'
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

@method_decorator(cache_control(private=True), name='dispatch')
class EmployeeDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_hris'
    model = Employee

class EmployeeCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_employee'
    model = Employee
    form_class = EmployeeCreateForm

class EmployeeUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_employee'
    model = Employee
    fields = '__all__'
    template_name_suffix = '_update_form'

class EmployeeDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_employee'
    model = Employee
    success_url = reverse_lazy('employees')

class PositionListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_hris'
    model = Position
    paginate_by = 10

class PositionDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_hris'
    model = Position

class PositionCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_position'
    model = Position
    fields = '__all__'

class PositionUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_position'
    model = Position
    fields = '__all__'
    template_name_suffix = '_update_form'

class PositionDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_position'
    model = Position
    success_url = reverse_lazy('positions')

class DepartmentListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_hris'
    model = Department
    paginate_by = 10

class DepartmentDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_hris'
    model = Department

class DepartmentCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_department'
    model = Department
    fields = '__all__'

class DepartmentUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_department'
    model = Department
    fields = '__all__'
    template_name_suffix = '_update_form'

class DepartmentDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_department'
    model = Department
    success_url = reverse_lazy('departments')

class MedicalAbstractListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = MedicalAbstract

class MedicalAbstractDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = MedicalAbstract

class MedicalAbstractCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_medicalabstract'
    model = MedicalAbstract
    fields = '__all__'

class MedicalAbstractUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_medicalabstract'
    model = MedicalAbstract
    fields = '__all__'
    template_name_suffix = '_update_form'

class MedicalAbstractDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_medicalabstract'
    model = MedicalAbstract
    success_url = reverse_lazy('medical-abstracts')
    
class DrugListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Drug
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(DrugListView, self).get_context_data(**kwargs)
        form = SearchForm()
        form.fields['query'].widget = forms.TextInput(
        attrs={
            'placeholder': 'Search Drugs...',
            'size': 32
            })
        context['form'] = form        
        return context


class DrugDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Drug

class DrugCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_drug'
    model = Drug
    fields = '__all__'

class DrugUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_drug'
    model = Drug
    fields = '__all__'
    template_name_suffix = '_update_form'

class DrugDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_drug'
    model = Drug
    success_url = reverse_lazy('drugs')

class MedicationListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Medication
    paginate_by = 10

class MedicationDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Medication

class MedicationCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_medication'
    model = Medication    
    form_class = MedicationCreateForm

class MedicationUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_medication'
    model = Medication
    form_class = MedicationCreateForm
    template_name_suffix = '_update_form'

class MedicationDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_medication'
    model = Medication
    success_url = reverse_lazy('medications')

class ItemListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_inventory'
    model = Item
    paginate_by = 10

class ItemDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_inventory'
    model = Item
