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
    path('nursing-home/search', views.search_page, name='search-page'),
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
    path('nursing-home/relationships/', views.RelationshipListView.as_view(), name='relationships'),
    path('nursing-home/relationship/<int:pk>/', views.RelationshipDetailView.as_view(), name='relationship-detail'),
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
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', login, {'template_name': 'registration/login.html', 'authentication_form': LoginForm}, name='login'),
    path('accounts/logout/', logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'media/(?P<path>.*)$',
            serve, {'document_root': settings.MEDIA_ROOT, }),
] 
