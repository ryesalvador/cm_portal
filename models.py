from django.db import models
from django.conf import settings
from django.urls import reverse

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

class Relative(models.Model):
    first_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35, blank=True)
    last_name = models.CharField(max_length=35)
    address = models.TextField(max_length=175, blank=True)
    relation = models.CharField(max_length=35, blank=True)
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
    #age 
    gender = models.CharField(max_length=1, choices=GENDER, blank=True)
    osca_id = models.CharField(max_length=24, blank=True)
    address = models.TextField(max_length=175)
    birth_date = models.DateField(auto_now=False)
    birth_place = models.CharField(max_length=35)
    nationality = models.CharField(max_length=70)
    civil_status = models.CharField(max_length=1, choices=CIVIL_STATUS, blank=True)
    most_recent_occupation = models.CharField(max_length=70, blank=True)
    date_and_time_of_admission = models.DateTimeField(auto_now=False, null=True, blank=True)
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
    died_on = models.DateField(auto_now=False, null=True, blank=True)
    discharged_on = models.DateField(auto_now=False, null=True, blank=True)    

    class Meta:
        ordering = ["last_name","first_name"]
        
    def __str__(self):
        return u'{1}, {0}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):        
        return reverse('resident-detail', args=[str(self.id)])
