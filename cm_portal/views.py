from django.shortcuts import render
from .models import Resident, Physician, Relative, Employee, Position, Department, \
     MedicalAbstract, Drug, Medication, Item, MedicalSupply, MedicalEquipment, \
     Charge, Building, ResidentWeight
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import ResidentCreateForm, EmployeeCreateForm, \
     MedicationCreateForm, MedicalSupplyCreateForm, MedicalEquipmentCreateForm, \
     UserUpdateForm, ChargeCreateForm, ResidentWeightCreateForm
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
     ResidentDeceasedTable, ResidentDischargedTable, ItemTable, MedicalSupplyTable, \
     MedicalEquipmentTable, ChargeTable, EmployeeTable
from django_tables2.export.views import ExportMixin
from .forms import SearchForm, DrugSearchForm

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
        'form': form, 'change_password': True
    })

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
        context['medicalabstract_list'] = MedicalAbstract.objects.all() 
        # HRIS
        context['employee_list'] = Employee.objects.all()
        context['position_list'] = Position.objects.all()
        context['department_list'] = Department.objects.all()      
        # CSU
        context['item_list'] = Item.objects.all()
        context['medicalequipment_list'] = MedicalEquipment.objects.all()
        context['medicalsupply_list'] = MedicalSupply.objects.all()
        context['charge_list'] = Charge.objects.all()
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
        return context

class CSUIndex(PermissionRequiredMixin, generic.base.TemplateView):
    permission_required = 'cm_portal.can_view_csu'
    template_name = 'cm_portal/csu_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_list'] = Item.objects.all()
        context['medicalequipment_list'] = MedicalEquipment.objects.all()
        context['medicalsupply_list'] = MedicalSupply.objects.all()
        context['charge_list'] = Charge.objects.all()
        return context

############################## GERIATRIC ##############################
##Resident views
class DeceasedResidentListView(PermissionRequiredMixin, tables.SingleTableView):    
    permission_required = 'cm_portal.can_view_nursing_home'    
    table_class = ResidentDeceasedTable
    queryset = Resident.objects.filter(vital_status='DE')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deceased'] = True
        return context

class DischargedResidentListView(PermissionRequiredMixin, tables.SingleTableView):    
    permission_required = 'cm_portal.can_view_nursing_home'    
    table_class = ResidentDischargedTable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discharged'] = True
        return context
        
@method_decorator(cache_control(private=True), name='dispatch')
class ResidentListView(PermissionRequiredMixin, ExportMixin, tables.SingleTableView):    
    permission_required = 'cm_portal.can_view_nursing_home'    
    table_class = ResidentTable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of Residents'
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
                context['maintenance'] = True              
            elif reports == 'osca':
                self.template_name = 'cm_portal/osca.html'
                context['osca'] = True
        else:
            context['resident'] = True
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

##Relative views
class RelativeListView(PermissionRequiredMixin, tables.SingleTableView):
    permission_required = 'cm_portal.can_view_nursing_home'
    table_class = RelativeTable    
    queryset = Relative.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['relative'] = True
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

##Physician views
class PhysicianListView(LoginRequiredMixin, tables.SingleTableView):
    permission_required = 'cm_portal.can_view_nursing_home'       
    table_class = PhysicianTable    
    queryset = Physician.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['physician'] = True
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
        context['drug'] = True
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

class MedicationDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Medication

class MedicationCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.add_medication'
    model = Medication
    form_class = MedicationCreateForm    
    
    def get_form(self, *args, **kwargs):
        form = super(MedicationCreate, self).get_form(*args, **kwargs)
        if 'pk' in self.kwargs:
            try:
              resident = Resident.objects.get(id=self.kwargs['pk'])
              form.fields['resident'].initial = resident
            except Resident.DoesNotExist:
              pass        
        return form

class MedicationUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.change_medication'
    model = Medication
    form_class = MedicationCreateForm
    template_name_suffix = '_update_form'

class MedicationDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.delete_medication'
    model = Medication
    success_url = reverse_lazy('medications')

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
    permission_required = 'cm_portal.can_view_nursing_home'
    model = ResidentWeight
    form_class = ResidentWeightCreateForm

class ResidentWeightUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = ResidentWeight
    form_class = ResidentWeightCreateForm
    template_name_suffix = '_update_form'

class ResidentWeightDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = ResidentWeight
    success_url = reverse_lazy('resident-weights')

##Building views
class BuildingListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Building
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building'] = True
        return context

class BuildingDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Building

class BuildingCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Building
    fields = '__all__'

class BuildingUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Building
    fields = '__all__'
    template_name_suffix = '_update_form'

class BuildingDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Building
    success_url = reverse_lazy('buildings')

############################## HRIS ##############################    
##Employee views
@method_decorator(cache_control(private=True), name='dispatch')
class EmployeeListView(PermissionRequiredMixin, tables.SingleTableView):
    permission_required = 'cm_portal.can_view_hris'
    table_class = EmployeeTable    
    queryset = Employee.objects.all()

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

############################## CSU ##############################
##Item views
class ItemListView(PermissionRequiredMixin, tables.SingleTableView):
    permission_required = 'cm_portal.can_view_csu'
    table_class = ItemTable    
    queryset = Item.objects.all()

class ItemDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_csu'
    model = Item

class ItemCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.can_view_csu'
    model = Item
    fields = '__all__'

class ItemUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.can_view_csu'
    model = Item
    fields = '__all__'
    template_name_suffix = '_update_form'

class ItemDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.can_view_csu'
    model = Item
    success_url = reverse_lazy('items')

##Medical supply views
class MedicalSupplyListView(PermissionRequiredMixin, tables.SingleTableView):
    permission_required = 'cm_portal.can_view_csu'
    table_class = MedicalSupplyTable    
    queryset = MedicalSupply.objects.all()

class MedicalSupplyDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_csu'
    model = MedicalSupply

class MedicalSupplyCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.can_view_csu'
    model = MedicalSupply
    form_class = MedicalSupplyCreateForm

class MedicalSupplyUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.can_view_csu'
    model = MedicalSupply
    form_class = MedicalSupplyCreateForm
    template_name_suffix = '_update_form'

class MedicalSupplyDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.can_view_csu'
    model = MedicalSupply
    success_url = reverse_lazy('medical-supplies')

##Medical equipment views
class MedicalEquipmentListView(PermissionRequiredMixin, tables.SingleTableView):
    permission_required = 'cm_portal.can_view_csu'
    table_class = MedicalEquipmentTable
    queryset = MedicalEquipment.objects.all()

class MedicalEquipmentDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_csu'
    model = MedicalEquipment

class MedicalEquipmentCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.can_view_csu'
    model = MedicalEquipment
    form_class = MedicalEquipmentCreateForm

class MedicalEquipmentUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.can_view_csu'
    model = MedicalEquipment
    form_class = MedicalEquipmentCreateForm
    template_name_suffix = '_update_form'

class MedicalEquipmentDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.can_view_csu'
    model = MedicalEquipment
    success_url = reverse_lazy('medical-equipments')

##Charge view
class ChargeListView(PermissionRequiredMixin, tables.SingleTableView):
    permission_required = 'cm_portal.can_view_csu'
    table_class = ChargeTable
    queryset = Charge.objects.all()

class ChargeDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_csu'
    model = Charge

class ChargeCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.can_view_csu'
    form_class = ChargeCreateForm
    model = Charge

    def get_form(self, *args, **kwargs):
        form = super(ChargeCreate, self).get_form(*args, **kwargs)
        if 'pk' in self.kwargs:
            try:
              item = MedicalSupply.objects.get(id=self.kwargs['pk'])
              user = self.request.user              
              form.fields['item'].initial = item
              form.fields['unit_of_measure'].initial = item.unit_of_measure
              form.fields['cashier'].initial = user
            except MedicalSupply.DoesNotExist:
              pass        
        return form

class ChargeDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.can_view_csu'
    model = Charge
    success_url = reverse_lazy('charges')

############################## USER ##############################    
##User view
class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'cm_portal/user_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail'] = True
        return context

class UserUpdate(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('index')
    template_name = 'cm_portal/user_update_form.html'

    def get_object(self):
        return self.request.user
