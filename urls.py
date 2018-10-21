from django.urls import path, include, re_path
from . import views
from django.contrib.auth.views import login, logout
from .forms import LoginForm

from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', views.index, name='index'),    
]

urlpatterns += [
    path('nursing-home/', views.nursing_home_index, name='nursing-home-index'),    
    path('nursing-home/residents/', views.ResidentListView.as_view(paginate_by=10), name='residents'),
    path('nursing-home/residents/order-by/building/', views.ResidentListView.as_view(
        template_name='cm_portal/resident_list_by_building.html'), name='resident-list-by-building'),
    path('nursing-home/residents/deceased/', views.DeceasedListView.as_view(), name='residents-deceased'),
    path('nursing-home/residents/discharged/', views.DischargedListView.as_view(), name='residents-discharged'),
    path('nursing-home/resident/<int:pk>/', views.ResidentDetailView.as_view(), name='resident-detail'),
    path('nursing-home/resident/create/', views.ResidentCreate.as_view(), name='resident-create'),
    path('nursing-home/resident/<int:pk>/update/', views.ResidentUpdate.as_view(), name='resident-update'),
    path('nursing-home/resident/<int:pk>/delete/', views.ResidentDelete.as_view(), name='resident-delete'),
    path('nursing-home/physicians/', views.PhysicianListView.as_view(), name='physicians'),
    path('nursing-home/physician/<int:pk>/', views.PhysicianDetailView.as_view(), name='physician-detail'),
    path('nursing-home/physician/create/', views.PhysicianCreate.as_view(), name='physician-create'),
    path('nursing-home/physician/<int:pk>/update/', views.PhysicianUpdate.as_view(), name='physician-update'),
    path('nursing-home/physician/<int:pk>/delete/', views.PhysicianDelete.as_view(), name='physician-delete'),
    path('nursing-home/relatives/', views.RelativeListView.as_view(), name='relatives'),
    path('nursing-home/relative/<int:pk>/', views.RelativeDetailView.as_view(), name='relative-detail'),
    path('nursing-home/relative/create/', views.RelativeCreate.as_view(), name='relative-create'),
    path('nursing-home/relative/<int:pk>/update/', views.RelativeUpdate.as_view(), name='relative-update'),
    path('nursing-home/relative/<int:pk>/delete/', views.RelativeDelete.as_view(), name='relative-delete'),
    path('nursing-home/relationships/', views.RelationshipListView.as_view(), name='relationships'),
    path('nursing-home/relationship/<int:pk>/', views.RelationshipDetailView.as_view(), name='relationship-detail'),
    path('nursing-home/relationship/create/', views.RelationshipCreate.as_view(), name='relationship-create'),
    path('nursing-home/relationship/<int:pk>/update/', views.RelationshipUpdate.as_view(), name='relationship-update'),
    path('nursing-home/relationship/<int:pk>/delete/', views.RelationshipDelete.as_view(), name='relationship-delete'),
    path('nursing-home/medical-abstracts/', views.MedicalAbstractListView.as_view(), name='medical-abstracts'),
    path('nursing-home/medical-abstract/<int:pk>/', views.MedicalAbstractDetailView.as_view(), name='medical-abstract-detail'),
    path('nursing-home/medical-abstract/create/', views.MedicalAbstractCreate.as_view(), name='medicalabstract-create'),
    path('nursing-home/medical-abstract/<int:pk>/update/', views.MedicalAbstractUpdate.as_view(), name='medicalabstract-update'),
    path('nursing-home/medical-abstract/<int:pk>/delete/', views.MedicalAbstractDelete.as_view(), name='medicalabstract-delete'),
    path('nursing-home/drugs/', views.DrugListView.as_view(), name='drugs'),
    path('nursing-home/drug/<int:pk>/', views.DrugDetailView.as_view(), name='drug-detail'),
    path('nursing-home/drug/create/', views.DrugCreate.as_view(), name='drug-create'),
    path('nursing-home/drug/<int:pk>/update/', views.DrugUpdate.as_view(), name='drug-update'),
    path('nursing-home/drug/<int:pk>/delete/', views.DrugDelete.as_view(), name='drug-delete'),
    path('nursing-home/medications/', views.MedicationListView.as_view(), name='medications'),
    path('nursing-home/medications/inventory/', views.maintenance, name='maintenance'),
    path('nursing-home/medication/<int:pk>/', views.MedicationDetailView.as_view(), name='medication-detail'),
    path('nursing-home/medication/create/', views.MedicationCreate.as_view(), name='medication-create'),
    path('nursing-home/medication/<int:pk>/update/', views.MedicationUpdate.as_view(), name='medication-update'),
    path('nursing-home/medication/<int:pk>/delete/', views.MedicationDelete.as_view(), name='medication-delete'),
]

urlpatterns += [
    path('nursing-home/search/residents', views.search, {'model': 'Resident', 'template_name': 'search_residents.html'}, name='search-residents'),
    path('nursing-home/search/relatives', views.search, {'model': 'Relative', 'template_name': 'search_relatives.html'}, name='search-relatives'),
    path('nursing-home/search/physicians', views.search, {'model': 'Physician', 'template_name': 'search_physicians.html'}, name='search-physicians'),
    path('nursing-home/search/drugs', views.search, {'model': 'Drug', 'template_name': 'search_drugs.html'}, name='search-drugs'),
]

urlpatterns += [
    path('hris/', views.hris_index, name='hris-index'),
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
    path('inventory/', views.inventory_index, name='inventory-index'),
    path('inventory/items/', views.ItemListView.as_view(), name='items'),
    path('inventory/item/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('inventory/item/create/', views.ItemCreate.as_view(), name='item-create'),
    path('inventory/item/<int:pk>/update/', views.ItemUpdate.as_view(), name='item-update'),
    path('inventory/item/<int:pk>/delete/', views.ItemDelete.as_view(), name='item-delete'),
    path('inventory/medical-supplies/', views.MedicalSupplyListView.as_view(), name='medical-supplies'),
    path('inventory/medical-supply/<uuid:pk>/', views.MedicalSupplyDetailView.as_view(), name='medicalsupply-detail'),
    path('inventory/medical-supply/create/', views.MedicalSupplyCreate.as_view(), name='medicalsupply-create'),
    path('inventory/medical-supply/<uuid:pk>/update/', views.MedicalSupplyUpdate.as_view(), name='medicalsupply-update'),
    path('inventory/medical-supply/<uuid:pk>/delete/', views.MedicalSupplyDelete.as_view(), name='medicalsupply-delete'),
    path('inventory/medical-equipments/', views.MedicalEquipmentListView.as_view(), name='medical-equipments'),
    path('inventory/medical-equipment/<uuid:pk>/', views.MedicalEquipmentDetailView.as_view(), name='medicalequipment-detail'),
    path('inventory/medical-equipment/create/', views.MedicalEquipmentCreate.as_view(), name='medicalequipment-create'),
    path('inventory/medical-equipment/<uuid:pk>/update/', views.MedicalEquipmentUpdate.as_view(), name='medicalequipment-update'),
    path('inventory/medical-equipment/<uuid:pk>/delete/', views.MedicalEquipmentDelete.as_view(), name='medicalequipment-delete'),
]

urlpatterns += [
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', login, {'template_name': 'registration/login.html', 'authentication_form': LoginForm}, name='login'),
    path('accounts/logout/', logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'media/(?P<path>.*)$',
            serve, {'document_root': settings.MEDIA_ROOT, }),
] 
