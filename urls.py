from django.urls import path, include, re_path, reverse
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.conf import settings
from django.views.static import serve
from cm_portal.models import Resident

urlpatterns = [
    path('', views.Dashboard.as_view(), name='index'),    
]

urlpatterns += [
    path('geriatric/', views.GeriatricIndex.as_view(), name='geriatric-index'),    
    path('geriatric/residents/', views.ResidentListView.as_view(
        template_name='cm_portal/residents.html',
        queryset=Resident.objects.filter(vital_status='LI'),
        paginate_by=10), name='residents'),    
    path('geriatric/residents/deceased/', views.ResidentListView.as_view(
        template_name='cm_portal/resident_list_deceased.html',
        queryset=Resident.objects.filter(vital_status='DE').order_by('-died_on')), name='residents-deceased'),    
    path('geriatric/residents/discharged/', views.ResidentListView.as_view(
        template_name='cm_portal/resident_list_discharged.html',
        queryset=Resident.objects.filter(vital_status='DC').order_by('-discharged_on')), name='residents-discharged'),        
    path('geriatric/resident/<int:pk>/', views.ResidentDetailView.as_view(), name='resident-detail'),
    path('geriatric/resident/create/', views.ResidentCreate.as_view(), name='resident-create'),
    path('geriatric/resident/<int:pk>/update/', views.ResidentUpdate.as_view(), name='resident-update'),
    path('geriatric/resident/<int:pk>/delete/', views.ResidentDelete.as_view(), name='resident-delete'),
    path('geriatric/physicians/', views.PhysicianListView.as_view(), name='physicians'),
    path('geriatric/physician/<int:pk>/', views.PhysicianDetailView.as_view(), name='physician-detail'),
    path('geriatric/physician/create/', views.PhysicianCreate.as_view(), name='physician-create'),
    path('geriatric/physician/<int:pk>/update/', views.PhysicianUpdate.as_view(), name='physician-update'),
    path('geriatric/physician/<int:pk>/delete/', views.PhysicianDelete.as_view(), name='physician-delete'),
    path('geriatric/relatives/', views.RelativeListView.as_view(), name='relatives'),
    path('geriatric/relative/<int:pk>/', views.RelativeDetailView.as_view(), name='relative-detail'),
    path('geriatric/relative/create/', views.RelativeCreate.as_view(), name='relative-create'),
    path('geriatric/relative/<int:pk>/update/', views.RelativeUpdate.as_view(), name='relative-update'),
    path('geriatric/relative/<int:pk>/delete/', views.RelativeDelete.as_view(), name='relative-delete'),    
    path('geriatric/medical-abstracts/', views.MedicalAbstractListView.as_view(), name='medical-abstracts'),
    path('geriatric/medical-abstract/<int:pk>/', views.MedicalAbstractDetailView.as_view(), name='medical-abstract-detail'),
    path('geriatric/medical-abstract/create/', views.MedicalAbstractCreate.as_view(), name='medicalabstract-create'),
    path('geriatric/medical-abstract/create/<int:pk>', views.MedicalAbstractCreate.as_view(), name='medicalabstract-create'),
    path('geriatric/medical-abstract/<int:pk>/update/', views.MedicalAbstractUpdate.as_view(), name='medicalabstract-update'),
    path('geriatric/medical-abstract/<int:pk>/delete/', views.MedicalAbstractDelete.as_view(), name='medicalabstract-delete'),
    path('geriatric/drugs/', views.DrugListView.as_view(), name='drugs'),
    path('geriatric/drug/<int:pk>/', views.DrugDetailView.as_view(), name='drug-detail'),
    path('geriatric/drug/create/', views.DrugCreate.as_view(), name='drug-create'),
    path('geriatric/drug/<int:pk>/update/', views.DrugUpdate.as_view(), name='drug-update'),
    path('geriatric/drug/<int:pk>/delete/', views.DrugDelete.as_view(), name='drug-delete'),
    path('geriatric/medications/', views.MedicationListView.as_view(), name='medications'),    
    path('geriatric/medication/<int:pk>/', views.MedicationDetailView.as_view(), name='medication-detail'),
    path('geriatric/medication/create/', views.MedicationCreate.as_view(), name='medication-create'),
    path('geriatric/medication/create/<int:pk>', views.MedicationCreate.as_view(), name='medication-create'),
    path('geriatric/medication/<int:pk>/update/', views.MedicationUpdate.as_view(), name='medication-update'),
    path('geriatric/medication/<int:pk>/delete/', views.MedicationDelete.as_view(), name='medication-delete'),
]

urlpatterns += [
    path('geriatric/search/', views.search, name='search'),    
]

urlpatterns += [
    path('hris/', views.HRISIndex.as_view(), name='hris-index'),
    path('hris/employees/', views.EmployeeListView.as_view(), name='employees'),
    path('hris/employee/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('hris/employee/create/', views.EmployeeCreate.as_view(), name='employee-create'),
    path('hris/employee/<int:pk>/update/', views.EmployeeUpdate.as_view(), name='employee-update'),
    path('hris/employee/<int:pk>/delete/', views.EmployeeDelete.as_view(), name='employee-delete'),
    path('hris/positions/', views.PositionListView.as_view(), name='positions'),
    path('hris/position/<int:pk>/', views.PositionDetailView.as_view(), name='position-detail'),
    path('hris/position/create/', views.PositionCreate.as_view(), name='position-create'),
    path('hris/position/<int:pk>/update/', views.PositionUpdate.as_view(), name='position-update'),
    path('hris/position/<int:pk>/delete/', views.PositionDelete.as_view(), name='position-delete'),
    path('hris/departments/', views.DepartmentListView.as_view(), name='departments'),
    path('hris/department/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
    path('hris/department/create/', views.DepartmentCreate.as_view(), name='department-create'),
    path('hris/department/<int:pk>/update/', views.DepartmentUpdate.as_view(), name='department-update'),
    path('hris/department/<int:pk>/delete/', views.DepartmentDelete.as_view(), name='department-delete'),
]

urlpatterns += [
    path('hris/search/employees', views.search, {'model': 'Employee', 'template_name': 'search_employees.html'}, name='search-employees'),    
]

urlpatterns += [
    path('csu/', views.CSUIndex.as_view(), name='csu-index'),
    path('csu/items/', views.ItemListView.as_view(), name='items'),
    path('csu/item/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('csu/item/create/', views.ItemCreate.as_view(), name='item-create'),
    path('csu/item/<int:pk>/update/', views.ItemUpdate.as_view(), name='item-update'),
    path('csu/item/<int:pk>/delete/', views.ItemDelete.as_view(), name='item-delete'),
    path('csu/medical-supplies/', views.MedicalSupplyListView.as_view(), name='medical-supplies'),
    path('csu/medical-supply/<uuid:pk>/', views.MedicalSupplyDetailView.as_view(), name='medicalsupply-detail'),
    path('csu/medical-supply/create/', views.MedicalSupplyCreate.as_view(), name='medicalsupply-create'),
    path('csu/medical-supply/<uuid:pk>/update/', views.MedicalSupplyUpdate.as_view(), name='medicalsupply-update'),
    path('csu/medical-supply/<uuid:pk>/delete/', views.MedicalSupplyDelete.as_view(), name='medicalsupply-delete'),
    path('csu/medical-equipments/', views.MedicalEquipmentListView.as_view(), name='medical-equipments'),
    path('csu/medical-equipment/<uuid:pk>/', views.MedicalEquipmentDetailView.as_view(), name='medicalequipment-detail'),
    path('csu/medical-equipment/create/', views.MedicalEquipmentCreate.as_view(), name='medicalequipment-create'),
    path('csu/medical-equipment/<uuid:pk>/update/', views.MedicalEquipmentUpdate.as_view(), name='medicalequipment-update'),
    path('csu/medical-equipment/<uuid:pk>/delete/', views.MedicalEquipmentDelete.as_view(), name='medicalequipment-delete'),
]

urlpatterns += [
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', LoginView.as_view(), {'template_name': 'registration/login.html', 'authentication_form': LoginForm}, name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'media/(?P<path>.*)$',
            serve, {'document_root': settings.MEDIA_ROOT, }),
] 
