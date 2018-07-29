from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django_dropbox_storage.storage import DropboxStorage

DROPBOX_STORAGE = DropboxStorage()

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

class Relationship(models.Model):
    related_to = models.ForeignKey('Resident', on_delete=models.CASCADE, null=True)
    relation = models.CharField(max_length=35, blank=True)

    def __str__(self):
        return u'{} of {} {}'.format(self.relation.capitalize(),
                                     self.related_to.first_name.capitalize(),
                                     self.related_to.last_name.capitalize())

    def get_absolute_url(self):
        return reverse('relationship-detail', args=[str(self.id)])

#Nursing Home Database Models
class Relative(models.Model):
    first_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35, blank=True)
    last_name = models.CharField(max_length=35)
    address = models.TextField(max_length=175, blank=True)
    relationship = models.ForeignKey('Relationship', on_delete=models.SET_NULL, null=True, blank=True)
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

class Resident(models.Model):
    first_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35, blank=True)
    last_name = models.CharField(max_length=35)
    photo = models.ImageField(
            null=True,
            blank=True,
            upload_to="photos/residents/%Y/%m/%D",
            storage=DROPBOX_STORAGE
            )
    #age
    gender = models.CharField(max_length=1, choices=GENDER, blank=True)
    osca_id = models.CharField(max_length=24, blank=True)
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
    room_number = models.CharField(max_length=70, blank=True)
    diet = models.TextField(blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    relatives = models.ManyToManyField(Relative)
    physicians = models.ManyToManyField(Physician, blank=True)
    vital_status = models.CharField(
        max_length=2,
        choices=VITAL_STATUS,
        default='LI'
        )
    died_on = models.DateTimeField(auto_now=False, null=True, blank=True)
    discharged_on = models.DateField(auto_now=False, null=True, blank=True)

    class Meta:
        ordering = ["last_name","first_name"]

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
            storage=DROPBOX_STORAGE
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

    def __str__(self):
        return u'{1}, {0}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('employee-detail', args=[str(self.id)])

class Position(models.Model):
    name = models.CharField(max_length=70)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    job_description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('position-detail', args=[str(self.id)])

class Department(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('department-detail', args=[str(self.id)])
