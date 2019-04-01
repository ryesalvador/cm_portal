import csv, django, os, datetime, sys
from django.apps import apps

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from cm_portal.models import *

myfile = open(sys.argv[1])
reader = csv.reader(myfile)
data = list(reader)

model = apps.get_model('cm_portal', sys.argv[2])

for i in data[1:]:
  d = {}
  for index, item in enumerate(i):    	
    d[data[0][index]] = item
  result = model.objects.create(**d)
