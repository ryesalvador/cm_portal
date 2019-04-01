import csv, django, os

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from cm_portal.models import Resident

of = open('output.csv', 'w', newline='')
ow = csv.writer(of)
ow.writerow(['Name', 'Medicine', 'Dosage', 'Frequency', 'Quantity', 'Due', 'Price'])

residents = Resident.objects.all()
context = {}

context['male_first_floor'] = residents.filter(building='1').filter(gender='M')
context['female_first_floor'] = residents.filter(building='1').filter(gender='F')
context['male_second_floor'] = residents.filter(building='2').filter(gender='M')
context['female_second_floor'] = residents.filter(building='2').filter(gender='F')
context['male_luigi_tezza'] = residents.filter(building='L').filter(gender='M')
context['female_luigi_tezza'] = residents.filter(building='L').filter(gender='F')
context['male_rebuschini'] = residents.filter(building='R').filter(gender='M')
context['female_rebuschini'] = residents.filter(building='R').filter(gender='F')

def export(d):
    for r in d:
        for m in r.medication_set.all():
            if m.medicine.brand_name:
                medicine = '{} ({})'.format(m.medicine.generic_name, m.medicine.brand_name)
            else:
                medicine = m.medicine.generic_name
            ow.writerow([r, medicine, \
            m.medicine.dosage, m.frequency, m.quantity, \
            m.due, m.medicine.price])

for k, v in context.items():
    export(context[k])

of.close()
