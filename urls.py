from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),    
]

urlpatterns += [
    path('nursing-home/', views.nursing_home_index, name='nursing-home-index'),
    path('nursing-home/residents/', views.ResidentListView.as_view(), name='residents'),
    path('nursing-home/resident/<int:pk>', views.ResidentDetailView.as_view(), name='resident-detail'),
    path('nursing-home/physicians/', views.PhysicianListView.as_view(), name='physicians'),
    path('nursing-home/physician/<int:pk>', views.PhysicianDetailView.as_view(), name='physician-detail'),
    path('nursing-home/relatives/', views.RelativeListView.as_view(), name='relatives'),
    path('nursing-home/relative/<int:pk>', views.RelativeDetailView.as_view(), name='relative-detail'),
]

urlpatterns += [
    path('hris/', views.hris_index, name='hris-index'),
    path('hris/employees/', views.EmployeeListView.as_view(), name='employees'),
    path('hris/employee/<int:pk>', views.EmployeeDetailView.as_view(), name='employee-detail'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
