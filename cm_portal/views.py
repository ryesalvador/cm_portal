from django.shortcuts import render
from .models import Resident, Physician, Relative, Employee, Position, Department, \
     MedicalAbstract, Drug, Medication, Item, MedicalSupply, MedicalEquipment
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import ResidentCreateForm, EmployeeCreateForm, \
     MedicationCreateForm, MedicalSupplyCreateForm, MedicalEquipmentCreateForm
from itertools import chain
from django.apps import apps
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from string import ascii_lowercase
from django.db.models.functions import Extract

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

class Dashboard(LoginRequiredMixin, generic.base.TemplateView):
    template_name = 'cm_portal/index.html'
    
class GeriatricIndex(PermissionRequiredMixin, generic.base.TemplateView):
    permission_required = 'cm_portal.can_view_nursing_home'
    template_name = 'cm_portal/geriatric_index.html'

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['resident_list'] = Resident.objects.filter(vital_status='LI')
        context['relative_list'] = Relative.objects.all()
        context['physician_list'] = Physician.objects.all()
        context['census_rebuschini'] = context['resident_list'].filter(building='R')
        context['census_luigi'] = context['resident_list'].filter(building='L')
        context['census_first_floor'] = context['resident_list'].filter(building='1')
        context['census_second_floor'] = context['resident_list'].filter(building='2')
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
    permission_required = 'cm_portal.can_view_inventory'
    template_name = 'cm_portal/csu_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_list'] = Item.objects.all()
        context['medicalequipment_list'] = MedicalEquipment.objects.all()
        context['medicalsupply_list'] = MedicalSupply.objects.all()        
        return context
    
@method_decorator(cache_control(private=True), name='dispatch')
class ResidentListView(PermissionRequiredMixin, generic.ListView):    
    permission_required = 'cm_portal.can_view_nursing_home'    
    #model is overriden by the urls.py which sets the queryset

    def filter_bldg(self, name, lst):
        return lst.filter(building=name)
    
    def filter_bday(self, month, lst):      
        return lst.annotate(birth_date_month = Extract('birth_date', 'month'),
                            birth_date_day = Extract('birth_date', 'day')
                            ).order_by('birth_date_month', 'birth_date_day').filter(birth_date__month=month)

    def filter_atoz(self, char, lst):
        return lst.filter(last_name__startswith=char)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'sort' in self.request.GET:
            sort = self.request.GET['sort'].strip()
            if sort == 'building':
                self.template_name = 'cm_portal/resident_list_by_building.html'
                context = {'rebuschini': 'R', 'tezza': 'L', 'first_floor': '1', 'second_floor': '2', 'bldg_three': '3'}
                for k, v in context.items():
                    context[k] = self.filter_bldg(v, self.queryset)                    
                return context
            elif sort == 'birthday':
                self.template_name = 'cm_portal/resident_list_by_birthday.html'
                context = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6,
                           'jul':7, 'aug':8, 'sept':9, 'oct':10, 'nov':11, 'dec':12}
                for k, v in context.items():
                    context[k] = self.filter_bday(v, self.queryset)
                return context
            elif sort == 'atoz':
                self.template_name = 'cm_portal/resident_list_by_a_to_z.html'
                context = {}
                for c in ascii_lowercase:
                    context[c] = c
                for k, v in context.items():
                    context[k] = self.filter_atoz(v, self.queryset)
                return context
            elif sort == 'admission':                                
                self.template_name = 'cm_portal/resident_list_by_admission.html'
                context['resident_list'] = self.queryset.order_by('-admission_date')
                return context
        elif 'reports' in self.request.GET:
            reports = self.request.GET['reports'].strip()
            if reports == 'maintenance':                
                self.template_name = 'cm_portal/maintenance.html'
                residents = self.queryset
                context['male_first_floor'] = residents.filter(building='1').filter(gender='M')
                context['female_first_floor'] = residents.filter(building='1').filter(gender='F')
                context['male_second_floor'] = residents.filter(building='2').filter(gender='M')
                context['female_second_floor'] = residents.filter(building='2').filter(gender='F')
                context['female_bldg_three'] = residents.filter(building='3').filter(gender='F')
                context['male_luigi_tezza'] = residents.filter(building='L').filter(gender='M')
                context['female_luigi_tezza'] = residents.filter(building='L').filter(gender='F')
                context['male_rebuschini'] = residents.filter(building='R').filter(gender='M')
                context['female_rebuschini'] = residents.filter(building='R').filter(gender='F')
                return context
            elif reports == 'osca':
                self.template_name = 'cm_portal/osca.html'                
                context = {'rebuschini': 'R', 'tezza': 'L', 'first_floor': '1', 'second_floor': '2'}
                for k, v in context.items():
                    context[k] = self.filter_bldg(v, self.queryset)
                return context
        #elif 'page' in self.request.GET:            
        #    self.template_name = 'cm_portal/resident_list.html'                    
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

@method_decorator(cache_control(private=True), name='dispatch')
class EmployeeListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_hris'
    model = Employee
    paginate_by = 10

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

class DrugListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Drug
    paginate_by = 10

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

class ItemListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_inventory'
    model = Item
    paginate_by = 10

class ItemDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_inventory'
    model = Item

class ItemCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.can_view_inventory'
    model = Item
    fields = '__all__'

class ItemUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.can_view_inventory'
    model = Item
    fields = '__all__'
    template_name_suffix = '_update_form'

class ItemDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.can_view_inventory'
    model = Item
    success_url = reverse_lazy('items')

class MedicalSupplyListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_inventory'
    model = MedicalSupply
    paginate_by = 10

class MedicalSupplyDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_inventory'
    model = MedicalSupply

class MedicalSupplyCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.can_view_inventory'
    model = MedicalSupply
    form_class = MedicalSupplyCreateForm

class MedicalSupplyUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.can_view_inventory'
    model = MedicalSupply
    form_class = MedicalSupplyCreateForm
    template_name_suffix = '_update_form'

class MedicalSupplyDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.can_view_inventory'
    model = MedicalSupply
    success_url = reverse_lazy('medical-supplies')

class MedicalEquipmentListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_inventory'
    model = MedicalEquipment
    paginate_by = 10

class MedicalEquipmentDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'cm_portal.can_view_inventory'
    model = MedicalEquipment

class MedicalEquipmentCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'cm_portal.can_view_inventory'
    model = MedicalEquipment
    form_class = MedicalEquipmentCreateForm

class MedicalEquipmentUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'cm_portal.can_view_inventory'
    model = MedicalEquipment
    form_class = MedicalEquipmentCreateForm
    template_name_suffix = '_update_form'

class MedicalEquipmentDelete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'cm_portal.can_view_inventory'
    model = MedicalEquipment
    success_url = reverse_lazy('medical-equipments')
