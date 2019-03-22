import csv, django, os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from cm_portal.models import Resident, Drug, Medication

myfile = open(sys.argv[1])
reader = csv.reader(myfile)
data = list(reader)

def extract(string, start='(', stop=')'):
    return string[string.index(start)+1:string.index(stop)]

for i in data[1:]:
    name = [x.strip() for x in i[0].split('\n')[0].split(',')]
    print(name)
    resident = Resident.objects.get(last_name=name[0], first_name=name[1])
    generic = i[1].split('(')[0]
    try:
        brand = extract(i[1].split()[-1])
    except:
        brand = ''
        #print('Generic name only')
    dosage = i[2]
    price = i[6]
    if price == '':
        price = 0
    frequency = i[3]

    quantity = i[4]
    if quantity == '':
        quantity = None
    elif quantity == 'DC':
        pass
    else:
        quantity = int(quantity)

    medicine = Drug.objects.get_or_create(generic_name=generic.title(),
                                   brand_name=brand,
                                   dosage=dosage)

    Drug.objects.filter(id=medicine[0].id).update(price=price)

    #print('{} - {} - {} - {}'.format(resident, medicine, frequency, quantity))

    medication = resident.medication_set.get_or_create(medicine=medicine[0], frequency=frequency)
    if quantity == 'DC':
        Medication.objects.filter(id=medication[0].id).delete()
    else:
        result = Medication.objects.filter(id=medication[0].id).update(quantity=quantity)
        print(result)
