import csv, django, os, sys
from django.apps import apps

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from cm_portal.models import *

of = open(sys.argv[2], 'w', newline='')
ow = csv.writer(of)

model = apps.get_model('cm_portal', sys.argv[1])
items = model.objects.all()

first = True
for item in items:
  fields = item.__dict__
  l = []
  if first:
    for f, v in fields.items():
    	l.append(f)
    ow.writerow(l)
    first = False
    l = []
  for f, v in fields.items():
    l.append(v)
  ow.writerow(l)
of.close()
