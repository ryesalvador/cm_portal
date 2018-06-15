from django.urls import path, include
from . import views
from django.contrib.auth.views import login, logout
from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),    
]

urlpatterns += [
    path('nursing-home/', views.nursing_home_index, name='nursing-home-index'),
    path('nursing-home/residents/', views.ResidentListView.as_view(), name='residents'),
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
    path('hris/departments/', views.DepartmentListView.as_view(), name='departments'),
    path('hris/department/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
]

urlpatterns += [
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', login, {'template_name': 'registration/login.html', 'authentication_form': LoginForm}, name='login'),
    path('accounts/logout/', logout),
]
