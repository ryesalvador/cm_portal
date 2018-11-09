from django.shortcuts import render
from .models import Resident, Physician, Relative, Relationship, \
     Employee, Position, Department, \
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def search(request):
    model = ''
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

    variables = {
            'model': model,
            'obj_list': obj_list,
            'show_results': show_results,
            }

    return render(request, 'cm_portal/search_geria.html', variables)


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
    context={'num_residents': num_residents,
             'num_physicians': num_physicians,
             'num_relatives': num_relatives,
             'census_rebuschini': census_rebuschini,
             'census_luigi': census_luigi,
             'census_first_floor': census_first_floor,
             'census_second_floor': census_second_floor,
             }
    return render(request, 'cm_portal/nursing_home_index.html', context)

@login_required
def ResidentListView(request):
    resident_list = Resident.objects.filter(vital_status='LI')

    def filter_bldg(name):
        return resident_list.filter(building=name)
    
    def filter_bday(month):
        return resident_list.filter(birth_date__month=month)
    
    if 'ajax' in request.GET and 'sort' in request.GET:
        sort = request.GET['sort'].strip()
        if sort and sort == 'bldg':                        
            context = {'rebuschini': 'R', 'tezza': 'L', 'first_floor': '1', 'second_floor': '2'}
            for k, v in context.items():
                context[k] = filter_bldg(v)
            return render(request, 'cm_portal/resident_list_by_building.html', context)
        elif sort == 'bday':
            context = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6,
                       'jul':7, 'aug':8, 'sept':9, 'oct':10, 'nov':11, 'dec':12}
            for k, v in context.items():
                context[k] = filter_bday(v)
            return render(request, 'cm_portal/resident_list_by_bday.html', context)                
    
    page = request.GET.get('page', 1)
    paginator = Paginator(resident_list, 10)

    try:
        resident_list = paginator.page(page)
    except PageNotAnInteger:
        resident_list = paginator.page(1)
    except EmptyPage:
        resident_list = paginator.page(paginator.num_pages)

    context = { 'resident_list': resident_list,
                'is_paginated': False }
    if paginator.num_pages > 1:
        context['is_paginated'] = True

    if 'ajax' in request.GET:
        return render(request, 'cm_portal/resident_list.html', context)
    else:
        return render(request, 'cm_portal/residents.html', context)

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
    num_medical_supplies = MedicalSupply.objects.all().count()
    num_medical_equipment = MedicalEquipment.objects.all().count()
    return render(request,
                  'cm_portal/inventory_index.html',
                  context={
                      'num_items': num_items,
                      'num_medical_supplies': num_medical_supplies,
                      'num_medical_equipment': num_medical_equipment
                      })

@login_required
def maintenance(request):
    male_first_floor = Resident.objects.filter(building='1').filter(gender='M').filter(vital_status='LI')
    female_first_floor = Resident.objects.filter(building='1').filter(gender='F').filter(vital_status='LI')
    male_second_floor = Resident.objects.filter(building='2').filter(gender='M').filter(vital_status='LI')
    female_second_floor = Resident.objects.filter(building='2').filter(gender='F').filter(vital_status='LI')
    male_luigi_tezza = Resident.objects.filter(building='L').filter(gender='M').filter(vital_status='LI')
    female_luigi_tezza = Resident.objects.filter(building='L').filter(gender='F').filter(vital_status='LI')
    male_rebuschini = Resident.objects.filter(building='R').filter(gender='M').filter(vital_status='LI')
    female_rebuschini = Resident.objects.filter(building='R').filter(gender='F').filter(vital_status='LI')
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
class DeceasedListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Resident
    queryset = Resident.objects.filter(vital_status='DE')
    template_name = 'cm_portal/resident_list_deceased.html'
    paginate_by = 10

@method_decorator(cache_control(private=True), name='dispatch')
class DischargedListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'cm_portal.can_view_nursing_home'
    model = Resident
    queryset = Resident.objects.filter(vital_status='DC')
    template_name = 'cm_portal/resident_list_discharged.html'
    paginate_by = 10

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
