from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('residents/', views.ResidentListView.as_view(), name='residents'),
    path('resident/<int:pk>', views.ResidentDetailView.as_view(), name='resident-detail'),
    path('physicians/', views.PhysicianListView.as_view(), name='physicians'),
    path('physician/<int:pk>', views.PhysicianDetailView.as_view(), name='physician-detail'),
    path('relatives/', views.RelativeListView.as_view(), name='relatives'),
    path('relative/<int:pk>', views.RelativeDetailView.as_view(), name='relative-detail'),
]
