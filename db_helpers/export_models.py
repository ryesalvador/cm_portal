import csv, django, os, sys
from django.apps import apps
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()
from cm_portal.models import *

def export_model(model, filename):
  o_file = open(filename, 'w', newline='')
  o_writer = csv.writer(o_file)
  items = model.objects.all()
  first = True
  for item in items:
    fields = item.__dict__
    l = []
    if first:
      for f, v in fields.items():
        l.append(f)
      o_writer.writerow(l)
      first = False
      l = []
    for f, v in fields.items():
      l.append(v)
    o_writer.writerow(l)
  o_file.close()

if __name__ == '__main__':
    if sys.argv[1]:
        for model in apps.get_models():
            if model._meta.app_label == sys.argv[1]:
                export_model(model, model.__name__ + '.csv')
    else:
        for model in apps.get_models():
            export_model(model, model.__name__ + '.csv')

