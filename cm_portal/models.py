from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
#from django_dropbox_storage.storage import DropboxStorage
from datetime import date
import uuid

#DROPBOX_STORAGE = DropboxStorage()

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    )

CIVIL_STATUS = (
    ('S', 'Single'),
    ('M', 'Married'),
    ('W', 'Widowed'),
    )

VITAL_STATUS = (
    ('LI', 'Assisted Living'),
    ('DE', 'Deceased'),
    ('DC', 'Discharged'),
    )

EMPLOYMENT_STATUS = (
        ('C', 'Contractual'),
        ('P', 'Probationary'),
        ('R', 'Regular'),
        ('W', 'Resigned'),
        ('T', 'Terminated'),
        )

EDUCATIONAL_ATTAINMENT = (
        ('G', 'Elementary Education'),
        ('H', 'High School'),
        ('U', 'Undergraduate'),
        ('C', 'College'),
        ('P', 'Post Graduate'),
        )

GRADE = (
        ('P', 'Poor'),
        ('F', 'Fair'),
        ('G', 'Good'),
        ('V', 'Very Good'),
        ('E', 'Excellent'),
        )

BUILDING = (
    ('R', 'Blessed Enrico Rebuschini Building'),
    ('L', 'Blessed Luigi Tezza Building'),
    ('1', 'St. Camillus Building - First floor'),
    ('2', 'St. Camillus Building - Second floor'),
    ('3', 'Building 3'),
    )

LEVEL_OF_CARE = (
    ('H', 'High'),
    ('I', 'Intermediate'),
    ('L', 'Low'),
    )

LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

ITEM_TYPE = (
        ('S', 'Medical Supply'),
        ('E', 'Medical Equipment'),
    )
   
#Geriatric Models   
class Clinic(models.Model):
	physician = models.ForeignKey('Physician', on_delete=models.CASCADE, blank=False)
	name_of_clinic = models.CharField(max_length=70)
	address = models.TextField(max_length=175)
	room = models.PositiveIntegerField(null=True, blank=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number_1 = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
	phone_number_2 = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	clinic_hours = models.TextField(max_length=140)
	
	def __str__(self):
		if self.room != None:
		    return u'{} - {} room {} | {}'.format(self.physician, self.name_of_clinic, self.room, self.clinic_hours)
		else:
			return u'{} - {} | {}'.format(self.physician, self.name_of_clinic, self.clinic_hours)
		
	def get_absolute_url(self):
		return reverse('clinic-detail', args=[str(self.id)])
			
class Physician(models.Model):
    first_name = models.CharField(max_length=35, verbose_name="name")
    middle_name = models.CharField(max_length=35, blank=True)
    last_name = models.CharField(max_length=35)
    specialties = models.CharField(max_length=175, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number_1 = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    phone_number_2 = models.CharField(validators=[phone_regex], max_length=17, blank=True)    
    mobile_number_1 = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    mobile_number_2 = models.CharField(validators=[phone_regex], max_length=17, blank=True)      

    class Meta:
        ordering = ["last_name","first_name"]

    def __str__(self):
        return u'Dr. {} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('physician-detail', args=[str(self.id)])
    
class Resident(models.Model):
    first_name = models.CharField(max_length=35, verbose_name="name")
    middle_name = models.CharField(max_length=35, blank=True)
    last_name = models.CharField(max_length=35)
    photo = models.ImageField(
            null=True,
            blank=True,
            upload_to="photos/residents/%Y/%m/%D",
            #storage=DROPBOX_STORAGE
            )
    #age
    gender = models.CharField(max_length=1, choices=GENDER, blank=True)
    osca_id = models.CharField(max_length=24, blank=True)
    philhealth = models.CharField(max_length=24, blank=True)
    address = models.TextField(max_length=175)
    birth_date = models.DateField(auto_now=False)
    birth_place = models.CharField(max_length=35)
    nationality = models.CharField(max_length=70)
    civil_status = models.CharField(max_length=1, choices=CIVIL_STATUS, blank=True)
    most_recent_occupation = models.CharField(max_length=70, blank=True)
    admission_date = models.DateField(auto_now=False, null=True, blank=True, verbose_name="date of admission")
    admission_time = models.TimeField(auto_now=False, null=True, blank=True, verbose_name="time of admission",)
    religion = models.CharField(max_length=70)
    reminders = models.TextField(blank=True)
    advanced_directives = models.CharField(max_length=70, blank=True)
    admitting_diagnosis = models.TextField(blank=True)
    level_of_care = models.CharField(max_length=1, choices=LEVEL_OF_CARE, blank=True)    
    residence = models.ForeignKey('Building', on_delete=models.CASCADE, null=True)
    room_number = models.CharField(max_length=70, blank=True)
    diet = models.TextField(blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)   
    physicians = models.ManyToManyField('Physician', blank=True)
    vital_status = models.CharField(
        max_length=2,
        choices=VITAL_STATUS,
        default='LI'
        )
    died_on = models.DateField(auto_now=False, null=True, blank=True)
    discharged_on = models.DateField(auto_now=False, null=True, blank=True)

    class Meta:
        ordering = ["last_name","first_name"]
        permissions = (("can_view_nursing_home", "View nursing home database"),
                       ("change_resident_diet", "Change resident's DIET ONLY"),)

    def __str__(self):
        return u'{1}, {0}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('resident-detail', args=[str(self.id)])

class Relative(models.Model):
    related_to = models.ForeignKey('Resident', on_delete=models.CASCADE, limit_choices_to={'vital_status': 'LI'}, null=True)
    relation_to_resident = models.CharField(max_length=35, blank=True)
    first_name = models.CharField(max_length=35, verbose_name="name")
    middle_name = models.CharField(max_length=35, blank=True)
    last_name = models.CharField(max_length=35)
    address = models.TextField(max_length=175, blank=True)    
    email = models.EmailField(null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number_1 = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    phone_number_2 = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    phone_number_3 = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    mobile_number_1 = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    mobile_number_2 = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    mobile_number_3 = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    class Meta:
        ordering = ["last_name","first_name"]        

    def __str__(self):
        return u'{1}, {0}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('relative-detail', args=[str(self.id)])
   
class MedicalAbstract(models.Model):
    resident = models.OneToOneField('Resident', on_delete=models.CASCADE, null=True)
    reason_for_confinement = models.TextField(blank=True)
    history_of_present_illness = models.TextField(blank=True)
    course_in_the_ward = models.TextField(blank=True)

    class Meta:
        ordering = ["resident"]

    def __str__(self):
        return u'{}'.format(self.resident)

    def get_absolute_url(self):
        return reverse('medical-abstract-detail', args=[str(self.id)])  
   
class Drug(models.Model):
    generic_name = models.CharField(max_length=70)
    brand_name = models.CharField(max_length=70, default='', blank=True)
    dosage = models.CharField(max_length=35, default='', blank=True)
    indication = models.TextField(blank=True)
    price = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["generic_name"]

    def __str__(self):
        if self.brand_name != '' and self.dosage != '':
            return u'{} ({}) - {}'.format(self.generic_name, self.brand_name, self.dosage)
        elif self.brand_name != '':
            return u'{} ({})'.format(self.generic_name, self.brand_name)
        elif self.dosage != '':
            return u'{} - {}'.format(self.generic_name, self.dosage)
        else:
            return self.generic_name

    def get_absolute_url(self):
        return reverse('drug-detail', args=[str(self.id)])

class Medication(models.Model):
    created = models.DateField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modified = models.DateField(auto_now=True, editable=False, null=False, blank=False)    
    resident = models.ForeignKey('Resident', on_delete=models.CASCADE, limit_choices_to={'vital_status': 'LI'}, null=True)
    medicine = models.ForeignKey('Drug', on_delete=models.CASCADE, null=True)
    frequency = models.CharField(max_length=70, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    discontinued = models.BooleanField(default=False)
    date_started = models.DateField(auto_now=False, null=True, blank=True)
    due = models.DateField(auto_now=False, null=True, blank=True)

    def __str__(self):
        return u'{} | {}'.format(self.resident, self.medicine)

    def get_absolute_url(self):
        return reverse('medication-detail', args=[str(self.id)])

class ResidentWeight(models.Model):
    resident = models.ForeignKey('Resident', on_delete=models.CASCADE, limit_choices_to={'vital_status': 'LI'}, null=True)
    date = models.DateField(auto_now=False, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["date"]        

    def __str__(self):
        return u'{0}: {1} - {2} Kg'.format(self.date, self.resident, self.weight)
    
    def get_absolute_url(self):
        return reverse('residentweight-detail', args=[str(self.id)])
    
class Building(models.Model):
    name = models.CharField(max_length=70)
    alias = models.CharField(max_length=70, default='', blank=True)

    class Meta:
        ordering = ["name"]        

    def __str__(self):
        return u'{0} ({1})'.format(self.name, self.alias)
    
    def get_absolute_url(self):
        return reverse('building-detail', args=[str(self.id)])
    
#Human Resource Information System Models
class Employee(models.Model):
    #Name
    first_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    photo = models.ImageField(
            null=True,
            blank=True,
            upload_to="photos/employees/%Y/%m/%D",
            #storage=DROPBOX_STORAGE
            )

    #Basic info
    gender = models.CharField(max_length=1, choices=GENDER, blank=True)
    civil_status = models.CharField(max_length=1, choices=CIVIL_STATUS, blank=True)
    birth_date = models.DateField(auto_now=False)
    permanent_address = models.TextField(max_length=175)
    educational_attainment = models.CharField(max_length=1, choices=EDUCATIONAL_ATTAINMENT, blank=True)

    #Contact
    contact_number = models.CharField(max_length=75)
    email = models.EmailField(null=True, blank=True)

    #Others
    social_security = models.CharField(max_length=24, blank=True)
    philhealth = models.CharField(max_length=24, blank=True)
    pagibig = models.CharField(max_length=24, blank=True)
    tin = models.CharField(max_length=24, blank=True)

    #Employment info
    position = models.ForeignKey('Position', on_delete=models.PROTECT, null=True)
    #date hired
    basic_salary = models.PositiveIntegerField(null=True, blank=True)
    allowance = models.PositiveIntegerField('Allowance/De Minimis', null=True, blank=True)
    monthly_salary = models.PositiveIntegerField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ["last_name","first_name"]
        permissions = (("can_view_hris", "View HRIS Database"),)

    def __str__(self):
        return u'{1}, {0}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('employee-detail', args=[str(self.id)])

class Position(models.Model):
    name = models.CharField(max_length=70)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    job_description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('position-detail', args=[str(self.id)])

class Department(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('department-detail', args=[str(self.id)])

class PerformanceAppraisal(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.PROTECT, null=True)
    evaluator = models.CharField(max_length=70)
    evaluation_type = models.CharField(max_length=70, blank=True)
    date = models.DateField(auto_now=False, default=timezone.now)
    result = models.CharField(max_length=1, choices=GRADE, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        ordering = ["employee"]

class EmploymentStatus(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    employment_status = models.CharField(max_length=1, choices=EMPLOYMENT_STATUS, default='C')
    date_started = models.DateField(auto_now=False)
    date_due = models.DateField(auto_now=False, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Employment statuses"
        ordering = ["date_started"]
    
    def __str__(self):
        return u'{} - {}'.format(self.employee, self.get_employment_status_display())
                
    def get_absolute_url(self):
        return reverse('employmentstatus-detail', args=[str(self.id)])
        
#Central Supplies Unit Models       
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def	get_absolute_url(self):
        return reverse('product-list-by-category',
                       args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def	get_absolute_url(self):
        return reverse('product-detail',
                       args=[self.id, self.slug])

class Order(models.Model):
    name = models.ForeignKey(Resident, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_absolute_url(self):
        return reverse('order-detail', args=[self.id])

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.Items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
            related_name='Items',
            on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
            related_name='order_items',
            on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
