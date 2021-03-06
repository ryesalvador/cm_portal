from django.shortcuts import render, reverse
from .models import Resident, Physician, Relative, Employee, Position, Department, \
     MedicalAbstract, Drug, Medication, Building, ResidentWeight, EmploymentStatus, \
     Clinic, OrderItem, Order
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import ResidentCreateForm, EmployeeCreateForm, \
     MedicationCreateForm, \
     UserUpdateForm, ResidentWeightCreateForm
from itertools import chain
from django.apps import apps
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from string import ascii_lowercase
from django.db.models.functions import Extract
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
import django_tables2 as tables
from .tables import ResidentTable, RelativeTable, PhysicianTable, DrugTable, \
     ResidentDeceasedTable, ResidentDischargedTable, \
     EmployeeTable
from django_tables2.export.views import ExportMixin
from .forms import SearchForm, DrugSearchForm, EmploymentStatusCreateForm, PhysicianSearchForm, ResidentUpdateDietForm, CartAddProductForm, OrderCreateForm

from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)
from dal import autocomplete
from django.db.models import Q
from datetime import datetime
from django.views.decorators.http import require_POST
from .cart import Cart

#Function-based views
@login_required
def search(request):    
    obj_list = []
    show_results = False

    if 'model' in request.GET and 'query' in request.GET:
        show_results = True
        model = request.GET['model'].strip()
        query = request.GET['query'].strip()
        if model and query:
            cls = apps.get_model('cm_portal', model)
            if model == 'drug':
                query0 = cls.objects.filter(generic_name__icontains=query)
                query1 = cls.objects.filter(brand_name__icontains=query)
            else:
                query0 = cls.objects.filter(last_name__icontains=query)
                query1 = cls.objects.filter(first_name__icontains=query)
            obj_list = list(chain(query0, query1))
        model = 'resident'

    variables = {
            'model': model,
            'obj_list': obj_list,
            'show_results': show_results,
            }

    return render(request, 'cm_portal/search_geria.html', variables)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user-detail', user.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cm_portal/change_password.html', {
        'form': form, 'highlight': 'change-password'
    })

@require_POST
@login_required
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                update_quantity=cd['update'])
    return redirect('cart-detail')

@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart-detail')

@login_required
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                initial={'quantity': item['quantity'],
                    'update': True})
    return render(request, 'cm_portal/cart/detail.html', {'cart': cart})

#Class-based views
class Dashboard(LoginRequiredMixin, generic.base.TemplateView):
    template_name = 'cm_portal/index.html'

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # Geriatric
        context['building_list'] = Building.objects.all() 
        context['resident_list'] = Resident.objects.filter(vital_status='LI')
        context['relative_list'] = Relative.objects.all()
        context['physician_list'] = Physician.objects.all()
        context['drug_list'] = Drug.objects.all()
        # HRIS
        context['employee_list'] = Employee.objects.all()
        context['position_list'] = Position.objects.all()
        context['department_list'] = Department.objects.all()      
        # CSU
        return context

##Main section views
class GeriatricIndex(PermissionRequiredMixin, generic.base.TemplateView):
    permission_required = 'cm_portal.can_view_nursing_home'
    template_name = 'cm_portal/geriatric_index.html'

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['resident_list'] = Resident.objects.filter(vital_status='LI')
        context['relative_list'] = Relative.objects.all()
        context['physician_list'] = Physician.objects.all()
        context['drug_list'] = Drug.objects.all()
        context['building_list'] = Building.objects.all()        
        return context

class HRISIndex(PermissionRequiredMixin, generic.base.TemplateView):
    permission_required = 'cm_portal.can_view_hris'
    template_name = 'cm_portal/hris_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_list'] = Employee.objects.all()
        context['position_list'] = Position.objects.all()
        context['department_list'] = Department.objects.all()  
        context['employmentstatus_list'] = EmploymentStatus.objects.all()      
        return context

class CSUIndex(PermissionRequiredMixin, generic.base.TemplateView):
    permission_required = 'cm_portal.can_view_csu'
    template_name = 'cm_portal/csu_index.html'

############################## GERIATRIC ##############################
##Resident views
class DeceasedResidentListView(PermissionRequiredMixin, tables.SingleTableView):    
    permission_required = 'cm_portal.can_view_nursing_home'    
    table_class = ResidentDeceasedTable
    queryset = Resident.objects.filter(vital_status='DE')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['highlight'] = 'deceased'
        return context

class DischargedResidentListView(PermissionRequiredMixin, tables.SingleTableView):    
    permission_required = 'cm_portal.can_view_nursing_home'    
    table_class = ResidentDischargedTable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['highlight'] = 'discharged'
        return context
        
@method_decorator(cache_control(private=True), name='dispatch')
class ResidentListView(PermissionRequiredMixin, ExportMixin, tables.SingleTableView):    
    permission_required = 'cm_portal.can_view_nursing_home'    
    table_class = ResidentTable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of Residents'
        context['highlight'] = 'residents'
        form = SearchForm(self.request.GET or {})        
        if 'q' in self.request.GET:
            query = self.request.GET['q'].strip()
            context['search'] = True
            context['title'] = 'Search Results for {}'.format(query)            
        if form.is_valid():          
            context['results'] = ResidentTable(form.get_queryset())          
        else:
            context['results'] = MyModel.objects.none()
        context['form'] = form        
        if 'reports' in self.request.GET:
            context['building_list'] = Building.objects.all()
            reports = self.request.GET['reports'].strip()
            if reports == 'maintenance':                
                self.template_name = 'cm_portal/maintenance.html'  
                context['highlight'] = 'maintenance'              
            elif reports == 'maintenance2':
                self.template_name = 'cm_portal/maintenance2.html'  
                context['date'] = datetime.today()              
            elif reports == 'osca':
                self.template_name = 'cm_portal/osca.html'
                context['highlight'] = 'osca'
        else:
            context['resident'] = True
        return context
    
@method_decorator(cache_control(private=True), name='dispatch')
class ResidentDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Resident

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'view' in self.request.GET:
            view = self.request.GET['view'].strip()
            if view == 'printable':
                self.template_name = 'cm_portal/resident_detail_printable.html'
        return context

class ResidentCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_resident'
    model = Resident
    form_class = ResidentCreateForm

class ResidentUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_resident'
    model = Resident
    form_class = ResidentCreateForm
    template_name_suffix = '_update_form'

class ResidentDietUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_resident_diet'
    model = Resident
    form_class = ResidentUpdateDietForm
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['diet'] = True
        return context

class ResidentDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_resident'
    model = Resident
    success_url = reverse_lazy('residents')

##Relative views
class RelativeListView(PermissionRequiredMixin, tables.SingleTableView):
    permission_required = 'cm_portal.can_view_nursing_home'
    table_class = RelativeTable    
    queryset = Relative.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['highlight'] = 'relatives'
        return context

class RelativeDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Relative

class RelativeCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_relative'
    model = Relative
    fields = '__all__'

    def get_form(self, *args, **kwargs):
        form = super(RelativeCreate, self).get_form(*args, **kwargs)
        if 'pk' in self.kwargs:
            try:
              resident = Resident.objects.get(id=self.kwargs['pk'])
              form.fields['related_to'].initial = resident
              self.success_url = reverse_lazy('resident-detail', kwargs={'pk': resident.id,})
            except Resident.DoesNotExist:
              pass        
        return form

class RelativeUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_relative'
    model = Relative
    fields = '__all__'
    template_name_suffix = '_update_form'

class RelativeDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_relative'
    model = Relative
    success_url = reverse_lazy('relatives')

##Physician views
class PhysicianListView(LoginRequiredMixin, tables.SingleTableView):
    permission_required = 'cm_portal.can_view_nursing_home'       
    table_class = PhysicianTable    
    queryset = Physician.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of Physicians'
        form = PhysicianSearchForm(self.request.GET or {})
        if 'q' in self.request.GET:
            query = self.request.GET['q'].strip()
            context['search'] = True
            context['title'] = 'Search Results for {}'.format(query)
        if form.is_valid():
            context['results'] = PhysicianTable(form.get_queryset())
        else:
            context['results'] = MyModel.objects.none()
        context['form'] = form
        context['highlight'] = 'physicians'
        return context

class PhysicianDetailView(LoginRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_nursing_home'
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

##Medical abstract views
class MedicalAbstractListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = MedicalAbstract
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medicalabstract'] = True
        return context

class MedicalAbstractDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = MedicalAbstract

class MedicalAbstractCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_medicalabstract'
    model = MedicalAbstract
    fields = '__all__'

    def get_form(self, *args, **kwargs):
        form = super(MedicalAbstractCreate, self).get_form(*args, **kwargs)
        if 'pk' in self.kwargs:
            try:
              resident = Resident.objects.get(id=self.kwargs['pk'])
              form.fields['resident'].initial = resident
            except Resident.DoesNotExist:
              pass        
        return form

class MedicalAbstractUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_medicalabstract'
    model = MedicalAbstract
    fields = '__all__'
    template_name_suffix = '_update_form'

class MedicalAbstractDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_medicalabstract'
    model = MedicalAbstract
    success_url = reverse_lazy('medical-abstracts')

##Drug views
class DrugAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Drug.objects.none()

        qs = Drug.objects.all()

        if self.q:
            qs = qs.filter(
                   Q(generic_name__istartswith=self.q) |
                   Q(brand_name__istartswith=self.q)
                  )
        return qs
 
class DrugListView(PermissionRequiredMixin, tables.SingleTableView):
    permission_required = 'cm_portal.can_view_nursing_home'
    table_class = DrugTable    
    queryset = Drug.objects.all()
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of Drugs'
        form = DrugSearchForm(self.request.GET or {})        
        if 'q' in self.request.GET:
            query = self.request.GET['q'].strip()
            context['search'] = True
            context['title'] = 'Search Results for {}'.format(query)            
        if form.is_valid():          
            context['results'] = DrugTable(form.get_queryset())          
        else:
            context['results'] = MyModel.objects.none()
        context['form'] = form 
        context['highlight'] = 'drugs'
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

##Medication views
class MedicationListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Medication
    paginate_by = 10

class MedicationDetailView(PermissionRequiredMixin, BSModalReadView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Medication
    template_name = 'cm_portal/medication_detail.html'

class MedicationCreate(PermissionRequiredMixin, BSModalCreateView):
    permission_required = 'cm_portal.add_medication'
    #model = Medication
    template_name = 'cm_portal/medication_form.html'
    form_class = MedicationCreateForm 
    success_message = 'Success: Medication was created.'
    #success_url = reverse_lazy('residents')   
    
    def get_form(self, *args, **kwargs):
        form = super(MedicationCreate, self).get_form(*args, **kwargs)
        if 'pk' in self.kwargs:
            try:
              resident = Resident.objects.get(id=self.kwargs['pk'])
              form.fields['resident'].initial = resident
              self.success_url = reverse_lazy('resident-detail', kwargs={'pk': resident.id,})
            except Resident.DoesNotExist:
              pass        
        return form

class MedicationUpdate(PermissionRequiredMixin, BSModalUpdateView):
    permission_required = 'cm_portal.change_medication'
    model = Medication
    template_name = 'cm_portal/bs4sdf_form.html'
    form_class = MedicationCreateForm
    success_message = 'Success: Medication was updated.'

    def get_object(self, *args, **kwargs):
        medication = super(MedicationUpdate, self).get_object(*args, **kwargs)
        resident = medication.resident
        self.success_url = reverse_lazy('resident-detail', kwargs={'pk': resident.id,})                
        return medication
    
    """def get_form(self, *args, **kwargs):
        form = super(MedicationUpdate, self).get_form(*args, **kwargs)
        if 'pk' in self.kwargs:
            try:
              medication = Medication.objects.get(id=self.kwargs['pk'])             
              resident = medication.resident
              self.success_url = reverse_lazy('resident-detail', kwargs={'pk': resident.id,})
            except Medication.DoesNotExist:
              pass        
        return form"""

class MedicationDelete(PermissionRequiredMixin, BSModalDeleteView):
    permission_required = 'cm_portal.delete_medication'
    model = Medication
    template_name = 'cm_portal/medication_confirm_delete.html'
    success_message = 'Success: Medication was deleted.'

    def get_object(self, *args, **kwargs):
        medication = super(MedicationDelete, self).get_object(*args, **kwargs)
        resident = medication.resident
        self.success_url = reverse_lazy('resident-detail', kwargs={'pk': resident.id,})                
        return medication

##Resident weight views
class ResidentWeightListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = ResidentWeight
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['residentweight'] = True
        return context

class ResidentWeightDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = ResidentWeight

class ResidentWeightCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_residentweight'
    model = ResidentWeight
    form_class = ResidentWeightCreateForm

class ResidentWeightUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_residentweight'
    model = ResidentWeight
    form_class = ResidentWeightCreateForm
    template_name_suffix = '_update_form'

class ResidentWeightDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_residentweight'
    model = ResidentWeight
    success_url = reverse_lazy('resident-weights')

##Building views
class BuildingListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Building
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['highlight'] = 'buildings'
        return context

class BuildingDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Building

class BuildingCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_building'
    model = Building
    fields = '__all__'

class BuildingUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_building'
    model = Building
    fields = '__all__'
    template_name_suffix = '_update_form'

class BuildingDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_building'
    model = Building
    success_url = reverse_lazy('buildings')
    
##Clinic views
class ClinicListView(PermissionRequiredMixin, generic.ListView):
	permission_required = 'cm_portal.can_view_nursing_home'
	model = Clinic
	paginate_by = 10
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['clinic'] = True
		return context
	
class ClinicDetailView(PermissionRequiredMixin, generic.DetailView):
	permission_required = 'cm_portal.can_view_nursing_home'
	model = Clinic

class ClinicCreate(PermissionRequiredMixin, generic.CreateView):
	permission_required = 'cm_portal.add_clinic'
	model = Clinic
	fields = '__all__'

class ClinicUpdate(PermissionRequiredMixin, generic.UpdateView):
	permission_required = 'cm_portal.change_clinic'
	model = Clinic
	fields = '__all__'
	template_name_suffix = '_update_form'

class ClinicDelete(PermissionRequiredMixin, generic.DeleteView):
	permission_required = 'cm_portal.delete_clinic'
	model = Clinic
	success_url = reverse_lazy('clinics')	

############################## HRIS ##############################    
##Employee views
@method_decorator(cache_control(private=True), name='dispatch')
class EmployeeListView(PermissionRequiredMixin, tables.SingleTableView):
    permission_required = 'cm_portal.can_view_hris'
    table_class = EmployeeTable    
    queryset = Employee.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['highlight'] = 'employees'
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

##Position views
class PositionListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_hris'
    model = Position
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['highlight'] = 'positions'
        return context

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

##Department views
class DepartmentListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_hris'
    model = Department
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['highlight'] = 'departments'
        return context

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
    
class EmploymentStatusListView(PermissionRequiredMixin, generic.ListView):
	permission_required = 'cm_portal.can_view_hris'
	model = EmploymentStatus
	paginate_by = 10
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['highlight'] = 'employmentstatuses'
		return context
	
class EmploymentStatusDetailView(PermissionRequiredMixin, generic.DetailView):
	permission_required = 'cm_portal.can_view_hris'
	model = EmploymentStatus
	
class EmploymentStatusCreate(PermissionRequiredMixin, generic.CreateView):
	permission_required = 'cm_portal.add_employmentstatus'
	model = EmploymentStatus
	form_class = EmploymentStatusCreateForm
	
class EmploymentStatusUpdate(PermissionRequiredMixin, generic.UpdateView):
	permission_required = 'cm_portal.change_employmentstatus'
	model = EmploymentStatus
	form_class = EmploymentStatusCreateForm
	template_name_suffix = '_update_form'
	
class EmploymentStatusDelete(PermissionRequiredMixin, generic.DeleteView):
	permission_required = 'cm_portal.delete_employmentstatus'
	model = EmploymentStatus
	success_url = reverse_lazy('employment-statuses')

############################## USER ##############################    
##User view
class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'cm_portal/user_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['highlight'] = 'user-detail'
        return context

class UserUpdate(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('index')
    template_name = 'cm_portal/user_update_form.html'

    def get_object(self):
        return self.request.user

from django.shortcuts import get_object_or_404
from .models import Category, Product
from .forms import CartAddProductForm

@login_required
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'cm_portal/product/list.html', {'category': category, 'categories': categories, 'products': products})

@login_required
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'cm_portal/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity'])
            cart.clear()
            return render(request,
                    'cm_portal/order/created.html',
                    {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
            'cm_portal/order/create.html',
            {'cart': cart, 'form': form})

@login_required
def order(request, id):
    order = get_object_or_404(Order, id=id)
    return render(request, 'cm_portal/order/order_detail.html', {'order': order})

