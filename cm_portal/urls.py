from django.urls import path, include, re_path, reverse
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.conf import settings
from django.views.static import serve
from cm_portal.models import Resident, Relative

urlpatterns = [
    path('', views.Dashboard.as_view(), name='index'),        
]

urlpatterns += [
    path('geriatric/', views.GeriatricIndex.as_view(), name='geriatric-index'),    
    path('geriatric/residents/', views.ResidentListView.as_view(
        queryset=Resident.objects.filter(vital_status='LI')), name='residents'),    
    path('geriatric/residents/deceased/', views.DeceasedResidentListView.as_view(
        template_name='cm_portal/deceasedresident_list.html',
        queryset=Resident.objects.filter(vital_status='DE').order_by('-died_on')), name='residents-deceased'),    
    path('geriatric/residents/discharged/', views.DischargedResidentListView.as_view(
        template_name='cm_portal/dischargedresident_list.html',
        queryset=Resident.objects.filter(vital_status='DC').order_by('-discharged_on')), name='residents-discharged'),        
    path('geriatric/resident/<int:pk>/', views.ResidentDetailView.as_view(), name='resident-detail'),
    path('geriatric/resident/create/', views.ResidentCreate.as_view(), name='resident-create'),
    path('geriatric/resident/<int:pk>/update/', views.ResidentUpdate.as_view(), name='resident-update'),
    path('geriatric/resident-diet/<int:pk>/update/', views.ResidentDietUpdate.as_view(), name='resident-diet-update'),
    path('geriatric/resident/<int:pk>/delete/', views.ResidentDelete.as_view(), name='resident-delete'),
    path('geriatric/physicians/', views.PhysicianListView.as_view(), name='physicians'),
    path('geriatric/physician/<int:pk>/', views.PhysicianDetailView.as_view(), name='physician-detail'),    
    path('geriatric/physician/create/', views.PhysicianCreate.as_view(), name='physician-create'),
    path('geriatric/physician/<int:pk>/update/', views.PhysicianUpdate.as_view(), name='physician-update'),
    path('geriatric/physician/<int:pk>/delete/', views.PhysicianDelete.as_view(), name='physician-delete'),
    path('geriatric/relatives/', views.RelativeListView.as_view(
        queryset=Relative.objects.filter(related_to__vital_status='LI')), name='relatives'),
    path('geriatric/relative/<int:pk>/', views.RelativeDetailView.as_view(), name='relative-detail'),
    path('geriatric/relative/create/', views.RelativeCreate.as_view(), name='relative-create'),
    path('geriatric/relative/create/<int:pk>', views.RelativeCreate.as_view(), name='relative-create'),
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
    path('geriatric/drug-autocomplete/', views.DrugAutocomplete.as_view(), name='drug-autocomplete'),
    path('geriatric/medications/', views.MedicationListView.as_view(), name='medications'),    
    path('geriatric/medication/<int:pk>/', views.MedicationDetailView.as_view(), name='medication-detail'),
    path('geriatric/medication-modal/<int:pk>/', views.MedicationDetailView.as_view(
        template_name='cm_portal/medication_modal_detail.html'), name='medication-modal-detail'),
    path('geriatric/medication/create/', views.MedicationCreate.as_view(), name='medication-create'),
    path('geriatric/medication/create/<int:pk>', views.MedicationCreate.as_view(), name='medication-create'),
    path('geriatric/medication-modal/create/<int:pk>', views.MedicationCreate.as_view(
        template_name='cm_portal/medication_modal_form.html'), name='medication-modal-create'),
    path('geriatric/medication/<int:pk>/update/', views.MedicationUpdate.as_view(), name='medication-update'),
    path('geriatric/medication-modal/<int:pk>/update/', views.MedicationUpdate.as_view(
        template_name='cm_portal/medication_modal_update_form.html'), name='medication-modal-update'),
    path('geriatric/medication/<int:pk>/delete/', views.MedicationDelete.as_view(), name='medication-delete'),
    path('geriatric/medication-modal/<int:pk>/delete/', views.MedicationDelete.as_view(
        template_name='cm_portal/medication_modal_confirm_delete.html'), name='medication-modal-delete'),
    path('geriatric/resident-weights/', views.ResidentWeightListView.as_view(), name='resident-weights'),
    path('geriatric/resident-weight/<int:pk>/', views.ResidentWeightDetailView.as_view(), name='residentweight-detail'),
    path('geriatric/resident-weight/create/', views.ResidentWeightCreate.as_view(), name='residentweight-create'),
    path('geriatric/resident-weight/<int:pk>/update/', views.ResidentWeightUpdate.as_view(), name='residentweight-update'),
    path('geriatric/resident-weight/<int:pk>/delete/', views.ResidentWeightDelete.as_view(), name='residentweight-delete'),
    path('geriatric/buildings/', views.BuildingListView.as_view(), name='buildings'),
    path('geriatric/building/<int:pk>/', views.BuildingDetailView.as_view(), name='building-detail'),
    path('geriatric/building/create/', views.BuildingCreate.as_view(), name='building-create'),
    path('geriatric/building/<int:pk>/update/', views.BuildingUpdate.as_view(), name='building-update'),
    path('geriatric/building/<int:pk>/delete/', views.BuildingDelete.as_view(), name='building-delete'),
    path('geriatric/clinics/', views.ClinicListView.as_view(), name='clinics'),
    path('geriatric/clinic/<int:pk>/', views.ClinicDetailView.as_view(), name='clinic-detail'),
    path('geriatric/clinic/create/', views.ClinicCreate.as_view(), name='clinic-create'),
    path('geriatric/clinic/<int:pk>/update/', views.ClinicUpdate.as_view(), name='clinic-update'),
    path('geriatric/clinic/<int:pk>/delete/', views.ClinicDelete.as_view(), name='clinic-delete'),
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
    path('hris/employment-statuses/', views.EmploymentStatusListView.as_view(), name='employment-statuses'),
    path('hris/employment-status/<int:pk>/', views.EmploymentStatusDetailView.as_view(), name='employmentstatus-detail'),
    path('hris/employment-status/create/', views.EmploymentStatusCreate.as_view(), name='employmentstatus-create'),
    path('hris/employment-status/<int:pk>/update/', views.EmploymentStatusUpdate.as_view(), name='employmentstatus-update'),
    path('hris/employment-status/<int:pk>/delete/', views.EmploymentStatusDelete.as_view(), name='employmentstatus-delete'),
]

urlpatterns += [
    path('hris/search/employees', views.search, {'model': 'Employee', 'template_name': 'search_employees.html'}, name='search-employees'),    
]

urlpatterns += [
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', LoginView.as_view(), {'template_name': 'registration/login.html', 'authentication_form': LoginForm}, name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/user/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('accounts/user/update/', views.UserUpdate.as_view(), name='user-update'),
    path('accounts/password/', views.change_password, name='change-password'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'media/(?P<path>.*)$',
            serve, {'document_root': settings.MEDIA_ROOT, }),
] 

urlpatterns += [
    path('csu/products/', views.product_list, name='product-list'),
    path('csu/products/<slug:category_slug>/', views.product_list, name='product-list-by-category'),
    path('csu/products/<int:id>/<slug:slug>/', views.product_detail, name='product-detail'),
]

urlpatterns += [
        path('csu/cart/', views.cart_detail, name='cart-detail'),
        path('csu/cart/add/<int:product_id>/',
            views.cart_add,
            name='cart-add'),
        path('csu/cart/remove/<int:product_id>/',
            views.cart_remove,
            name='cart-remove'),
]

urlpatterns += [
    path('csu/order/<int:id>/', views.order, name='order-detail'),
    path('csu/orders/create', views.order_create, name='order-create'),        
]
