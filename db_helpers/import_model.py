import csv, django, os, datetime, sys
from django.apps import apps
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()
from cm_portal.models import *

myfile = open(sys.argv[1])
reader = csv.reader(myfile)
data = list(reader)
model = apps.get_model('cm_portal', sys.argv[2])

# Feel free to add yours
nullable_fields = ['DateField', 'FloatField', 'TimeField', 'PositiveIntegerField']

for i in data[1:]:
  d = {}
  for index, item in enumerate(i):    	
    field_type =  model._meta.get_field(data[0][index]).get_internal_type()
    if item == '':
      if field_type in nullable_fields:
        item = None
    d[data[0][index]] = item
  result = model.objects.create(**d)
  print(result)
