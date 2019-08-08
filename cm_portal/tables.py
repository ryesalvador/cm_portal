import django_tables2 as tables
from .models import Resident, Relative, Physician, Drug, \
     Item, MedicalSupply, MedicalEquipment, Charge, Employee
from django.utils.html import format_html

class PhotoColumn(tables.Column):    
    def render(self, value):
        print(value)
        return format_html('<img src="/media{}" width="50px" height="50px" />', value)
    
class ResidentTable(tables.Table):
    photo = PhotoColumn(accessor='photo', linkify=True)
    last_name = tables.Column(linkify=True)
    first_name = tables.Column(linkify=True)
    #middle_name = tables.Column(linkify=True)
    
    class Meta:
        model = Resident
        template_name = 'django_tables2/bootstrap4.html'
        sequence = ('last_name',
                    'first_name',)
        exclude = ('id',
                   'photo',
                   'gender',
                   'osca_id',
                   'philhealth',
                   'address',
                   'birth_place',
                   'nationality',
                   'civil_status',
                   'most_recent_occupation',
                   'admission_time',
                   'religion',
                   'reminders',
                   'advanced_directives',
                   'admitting_diagnosis',
                   'room_number',
                   'diet',
                   'weight',
                   'height',
                   'physicians',
                   'vital_status',
                   'died_on',
                   'discharged_on',)
        attrs = {'class': 'table table-hover'}

class ResidentDeceasedTable(tables.Table):
    photo = PhotoColumn(accessor='photo', linkify=True)
    last_name = tables.Column(linkify=True)
    first_name = tables.Column(linkify=True)
    #middle_name = tables.Column(linkify=True)
    
    class Meta:
        model = Resident
        template_name = 'django_tables2/bootstrap4.html'
        sequence = ('last_name',
                    'first_name',)
        exclude = ('id',  
                   'photo',                 
                   'gender',
                   'osca_id',
                   'philhealth',
                   'address',
                   'birth_place',
                   'nationality',
                   'civil_status',
                   'most_recent_occupation',
                   'admission_time',
                   'religion',
                   'reminders',
                   'advanced_directives',
                   'admitting_diagnosis',
                   'room_number',
                   'diet',
                   'weight',
                   'height',
                   'level_of_care',
                   'residence',
                   'physicians',
                   #'vital_status',
                   #'died_on',
                   'discharged_on',)
        attrs = {'class': 'table table-hover'}

class ResidentDischargedTable(tables.Table):
    photo = PhotoColumn(accessor='photo', linkify=True)
    last_name = tables.Column(linkify=True)
    first_name = tables.Column(linkify=True)
    #middle_name = tables.Column(linkify=True)
    
    class Meta:
        model = Resident
        template_name = 'django_tables2/bootstrap4.html'
        sequence = ('last_name',
                    'first_name',)
        exclude = ('id',                   
                   'photo',
                   'gender',
                   'osca_id',
                   'philhealth',
                   'address',
                   'birth_place',
                   'nationality',
                   'civil_status',
                   'most_recent_occupation',
                   'admission_time',
                   'religion',
                   'reminders',
                   'advanced_directives',
                   'admitting_diagnosis',
                   'room_number',
                   'diet',
                   'weight',
                   'height',
                   'level_of_care',
                   'residence',
                   'physicians',
                   #'vital_status',
                   'died_on',
                   #'discharged_on',
                   )
        attrs = {'class': 'table table-hover'}
        
class RelativeTable(tables.Table):
    last_name = tables.Column(linkify=True)
    first_name = tables.Column(linkify=True)
    
    class Meta:
        model = Relative
        template_name = 'django_tables2/bootstrap4.html'
        sequence = ('last_name',
                    'first_name',
                    'middle_name',
                    'related_to',
                    'relation_to_resident',)
        exclude = ('id', 'address',)
        attrs = {'class': 'table table-hover'}
        
class PhysicianTable(tables.Table):
    last_name = tables.Column(linkify=True)
    first_name = tables.Column(linkify=True)
    
    class Meta:
        model = Physician
        template_name = 'django_tables2/bootstrap4.html'
        sequence = ('last_name',
                    'first_name',)                   
        exclude = ('id',)
        attrs = {'class': 'table table-hover'}

class DrugTable(tables.Table):
    generic_name = tables.Column(linkify=True)
    brand_name = tables.Column(linkify=True)
    
    class Meta:
        model = Drug
        template_name = 'django_tables2/bootstrap4.html'
        exclude = ('id',
                   'indication',)
        attrs = {'class': 'table table-hover'}

class ItemTable(tables.Table):
    item_name = tables.Column(linkify=True)
    #brand_name = tables.Column(linkify=True)
    
    class Meta:
        model = Item
        template_name = 'django_tables2/bootstrap4.html'
        sequence = ('item_name',
                    'brand_name',                    
                    'model',
                    'manufacturer',
                    'item_type',
                    )
        exclude = ('id',
                   'description',)
        attrs = {'class': 'table table-hover'}

class MedicalSupplyTable(tables.Table):
    id = tables.Column(accessor='id', linkify=True)
    
    class Meta:
        model = MedicalSupply
        template_name = 'django_tables2/bootstrap4.html'        
        attrs = {'class': 'table table-hover'}

class MedicalEquipmentTable(tables.Table):
    id = tables.Column(accessor='id', linkify=True)
    
    class Meta:
        model = MedicalEquipment
        template_name = 'django_tables2/bootstrap4.html'        
        attrs = {'class': 'table table-hover'}

class ChargeTable(tables.Table):
    id = tables.Column(accessor='id', linkify=True)
    
    class Meta:
        model = Charge
        template_name = 'django_tables2/bootstrap4.html'        
        attrs = {'class': 'table table-hover'}

class EmployeeTable(tables.Table):
    last_name = tables.Column(linkify=True)
    first_name = tables.Column(linkify=True)
    class Meta:
        model = Employee
        template_name = 'django_tables2/bootstrap4.html'
        sequence = ('id',
                    'last_name',
                    'first_name',)
        exclude = (#'id',
                   'photo',
                   #'civil_status',
                   'permanent_address',
                   #'educational_attainment',
                   'contact_number',
                   'email',
                   'social_security',
                   'philhealth',
                   'pagibig',
                   'tin',
                   'basic_salary',
                   'allowance',
                   'remarks',
                   )
        attrs = {'class': 'table table-hover'}
