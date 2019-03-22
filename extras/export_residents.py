import csv, django, os
from cm_portal.models import Resident

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

of = open('residents.csv', 'w', newline='')
ow = csv.writer(of)
residents = Resident.objects.all().order_by('admission_date')

first = True
for resident in residents:
  fields = resident.__dict__
  c = 0  
  l = []  
  if first:
    for f, v in fields.items():
    	if c > 1:
    		l.append(f)
    	c += 1
    ow.writerow(l)
    first = False
    c = 0
    l = []
  for f, v in fields.items():  	   	 
    if c > 1:
      l.append(v)
    c += 1
  ow.writerow(l)  
    
of.close()