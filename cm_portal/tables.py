import django_tables2 as tables
from .models import Resident, Relative, Physician, Drug, \
     Employee
from django.utils.html import format_html

class PhotoColumn(tables.Column):    
    def render(self, value):
        print(value)
        return format_html('<img src="/media{}" width="50px" height="50px" />', value)
    
class ResidentTable(tables.Table):
    photo = PhotoColumn(accessor='photo', linkify=True)
    first_name = tables.Column(order_by=("last_name", "first_name"), linkify=True)
    
    def render_first_name(self, value, record):
        middle_initial = ''
        if not record.middle_name=='':
            middle_initial = record.middle_name[0] + '.'
        return format_html("<b>{}, {} {}</b>", record.last_name, value, middle_initial)
    
    class Meta:
        model = Resident
        template_name = 'django_tables2/bootstrap4.html'        
        exclude = ('id',
                   'last_name',
                   'middle_name',
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
    first_name = tables.Column(order_by=("last_name", "first_name"), linkify=True)
    
    def render_first_name(self, value, record):
        middle_initial = ''
        if not record.middle_name=='':
            middle_initial = record.middle_name[0] + '.'
        return format_html("<b>{}, {} {}</b>", record.last_name, value, middle_initial)

    class Meta:
        model = Resident
        template_name = 'django_tables2/bootstrap4.html' 
        sequence = ('first_name', 'birth_date', 'died_on')       
        exclude = ('id', 
                   'last_name',
                   'middle_name', 
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
                   'vital_status',
                   #'died_on',
                   'discharged_on',)
        attrs = {'class': 'table table-hover'}

class ResidentDischargedTable(tables.Table):
    photo = PhotoColumn(accessor='photo', linkify=True)
    first_name = tables.Column(order_by=("last_name", "first_name"), linkify=True)
    
    def render_first_name(self, value, record):
        middle_initial = ''
        if not record.middle_name=='':
            middle_initial = record.middle_name[0] + '.'
        return format_html("<b>{}, {} {}</b>", record.last_name, value, middle_initial)

    class Meta:
        model = Resident
        template_name = 'django_tables2/bootstrap4.html'        
        exclude = ('id', 
                   'last_name',
                   'middle_name',                 
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
    first_name = tables.Column(order_by=("last_name", "first_name"), linkify=True)

    def render_first_name(self, value, record):
        middle_initial = ''
        if not record.middle_name=='':
            middle_initial = record.middle_name[0] + '.'
        return format_html("<b>{}, {} {}</b>", record.last_name, value, middle_initial)
    
    class Meta:
        model = Relative
        template_name = 'django_tables2/bootstrap4.html'
        sequence = ('first_name',                    
                    'related_to',
                    'relation_to_resident',)
        exclude = ('id',
                   'last_name',
                   'middle_name',
                   'address',
                   'phone_number_2',
                   'phone_number_3',
                   'mobile_number_2',
                   'mobile_number_3',)
        attrs = {'class': 'table table-hover'}
        
class PhysicianTable(tables.Table):    
    first_name = tables.Column(order_by=("last_name", "first_name"), linkify=True)
    
    def render_first_name(self, value, record):
        middle_initial = ','
        if not record.middle_name=='':
            middle_initial = record.middle_name[0] + '.,'
        return format_html("<b>{}, {}{} M.D.</b>", record.last_name, value, middle_initial)
    
    class Meta:
        model = Physician
        template_name = 'django_tables2/bootstrap4.html'
        sequence = ('last_name',
                    'first_name',)                   
        exclude = ('id', 'last_name', 'middle_name', 'phone_number_2', 'mobile_number_2',)
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
