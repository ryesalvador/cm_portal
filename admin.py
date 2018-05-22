from django.contrib import admin
from .models import Relative, Physician, Resident

@admin.register(Relative)
class RelativeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'relation', 'telephone')
    search_fields = ('first_name', 'last_name')

@admin.register(Physician)
class PhysicianAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'telephone')
    search_fields = ('first_name', 'last_name')

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')
    filter_horizontal = ('relatives', 'physicians')
