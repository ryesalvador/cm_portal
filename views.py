from django.shortcuts import render
from .models import Resident, Physician, Relative
from django.views import generic

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

class ResidentListView(generic.ListView):
    model = Resident

class ResidentDetailView(generic.DetailView):
    model = Resident

class PhysicianListView(generic.ListView):
    model = Physician

class PhysicianDetailView(generic.DetailView):
    model = Physician

class RelativeListView(generic.ListView):
    model = Relative    

class RelativeDetailView(generic.DetailView):
    model = Relative
