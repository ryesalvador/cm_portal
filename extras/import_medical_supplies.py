import csv, django, os, datetime, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from cm_portal.models import Item, MedicalSupply

myfile = open(sys.argv[1])
reader = csv.reader(myfile)
data = list(reader)

def extract(string, start='(', stop=')'):
    return string[string.index(start)+1:string.index(stop)]

for i in data[1:]:
    name = i[0]
    brand = i[1]
    manufacturer = i[2]
    item = Item.objects.get_or_create(item_name=name, brand_name=brand,
                                      manufacturer=manufacturer)
    print(item)
    if i[3] != '':
        date_acquired = datetime.datetime.strptime(i[3], '%Y-%m-%d')
    else:
        date_acquired = None
    
    if i[4] != '':
        expiration_date = datetime.datetime.strptime(i[4], '%Y-%m-%d')
    else:
        expiration_date = None
    stocks_available = i[5]
    if stocks_available == '':
        stocks_available = None
    else:
        stocks_available = int(stocks_available)
    unit_of_measure = i[6]
   
    med_supply = MedicalSupply.objects.get_or_create(item=item[0],
        date_acquired=date_acquired,
        expiration_date=expiration_date,
        stocks_available=stocks_available,
        unit_of_measure=unit_of_measure)
    print(med_supply)

