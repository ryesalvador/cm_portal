from django.shortcuts import render
from .models import Resident, Physician, Relative

def index(request):
    num_residents = Resident.objects.all().count()
    num_physicians = Physician.objects.all().count()
    num_relatives = Relative.objects.all().count()

    return render(request,
            'cm_portal/index.html',
            context={
                'num_residents': num_residents,
                'num_physicians': num_physicians,
                'num_relatives': num_relatives
                })


