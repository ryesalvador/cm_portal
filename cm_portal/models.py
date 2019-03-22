from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
#from django_dropbox_storage.storage import DropboxStorage
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
    ('LI', 'Living'),
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

class Item(models.Model):
    item_type = models.CharField(max_length=1, choices=ITEM_TYPE, default='S')
    item_name = models.CharField(max_length=70)
    brand_name = models.CharField(max_length=70, blank=True)
    model = models.CharField(max_length=70, blank=True)
    manufacturer = models.CharField(max_length=70, blank=True)
    description = models.TextField(blank=True)    

    class Meta:
        ordering = ["item_name"]

    def __str__(self):
        return u'{}'.format(self.item_name)

    def get_absolute_url(self):
        return reverse('item-detail', args=[str(self.id)])

class MedicalSupply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular medical supply across whole inventory')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=True)    
    date_acquired = models.DateField(auto_now=False, null=True, blank=True)
    expiration_date = models.DateField(auto_now=False, null=True, blank=True)
    stocks_available = models.PositiveIntegerField(null=True, blank=True)
    unit_of_measure = models.CharField(max_length=35, blank=True)

    class Meta:
        verbose_name_plural = "Medical supplies"
        ordering = ["item"]

    def __str__(self):
        return u'{}'.format(self.item)

    def get_absolute_url(self):
        return reverse('medicalsupply-detail', args=[str(self.id)])

class MedicalEquipment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular medical equipment across whole inventory')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=1, choices=BUILDING, blank=True)
    date_acquired = models.DateField(auto_now=False, null=True, blank=True)
    due_back = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Medical equipment availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.item.item_name})'

    def get_absolute_url(self):
        return reverse('medicalequipment-detail', args=[str(self.id)])
    
class Drug(models.Model):
    generic_name = models.CharField(max_length=70)
    brand_name = models.CharField(max_length=70, default='', blank=True)
    dosage = models.CharField(max_length=35, default='', blank=True)
    indication = models.CharField(max_length=70, blank=True)
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
    
#Nursing Home Database Models
class Relative(models.Model):
    related_to = models.ForeignKey('Resident', on_delete=models.CASCADE, null=True)
    relation_to_resident = models.CharField(max_length=35, blank=True)
    first_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35, blank=True)
    last_name = models.CharField(max_length=35)
    address = models.TextField(max_length=175, blank=True)    
    telephone = models.CharField(max_length=75, blank=True)

    class Meta:
        ordering = ["last_name","first_name"]        

    def __str__(self):
        return u'{1}, {0}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('relative-detail', args=[str(self.id)])

class Physician(models.Model):
    first_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35, blank=True)
    last_name = models.CharField(max_length=35)
    specialty = models.CharField(max_length=35, blank=True)
    telephone = models.CharField(max_length=75)
    hospital_of_choice = models.TextField()

    class Meta:
        ordering = ["last_name","first_name"]

    def __str__(self):
        return u'Dr. {} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('physician-detail', args=[str(self.id)])

class ResidentWeight(models.Model):
    resident = models.ForeignKey('Resident', on_delete=models.CASCADE, limit_choices_to={'vital_status': 'LI'}, null=True)
    date = models.DateField(auto_now=False, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    
class Resident(models.Model):
    first_name = models.CharField(max_length=35)
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
    building = models.CharField(max_length=1, choices=BUILDING, blank=True)
    room_number = models.CharField(max_length=70, blank=True)
    diet = models.TextField(blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)   
    physicians = models.ManyToManyField(Physician, blank=True)
    vital_status = models.CharField(
        max_length=2,
        choices=VITAL_STATUS,
        default='LI'
        )
    died_on = models.DateField(auto_now=False, null=True, blank=True)
    discharged_on = models.DateField(auto_now=False, null=True, blank=True)

    class Meta:
        ordering = ["last_name","first_name"]
        permissions = (("can_view_nursing_home", "View nursing home database"),)

    def __str__(self):
        return u'{1}, {0}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('resident-detail', args=[str(self.id)])


#Human Resource Information System Models
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

    def __str__(self):
        return str(self.date_started)

    class Meta:
        verbose_name_plural = "Employment statuses"
        ordering = ["date_started"]

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
