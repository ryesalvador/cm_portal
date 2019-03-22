import csv, django, os, datetime, sys
from cm_portal.models import Resident
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()
myfile = open(sys.argv[1])
reader = csv.reader(myfile)
data = list(reader)
for i in data[1:]:
  d = {}
  for index, item in enumerate(i):    	
    if data[0][index] == 'admission_date' and item == '':
      item = None 
    elif data[0][index] == 'admission_time' and item == '':
      item = None
    elif data[0][index] == 'weight' and item == '':
      item = None
    elif data[0][index] == 'height' and item == '':
      item = None
    elif data[0][index] == 'died_on' and item == '':
      item = None
    elif data[0][index] == 'discharged_on' and item == '':
      item = None
    d[data[0][index]] = item
  r = Resident.objects.create(**d)


	