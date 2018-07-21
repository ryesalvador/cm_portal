from django.contrib import admin
from .models import Relative, Physician, Resident, Relationship, \
     PerformanceAppraisal, EmploymentStatus, Employee, Position, Department

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    pass

@admin.register(Relative)
class RelativeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'relationship', 'telephone')
    search_fields = ('first_name', 'last_name')
    
@admin.register(Physician)
class PhysicianAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'telephone')
    search_fields = ('first_name', 'last_name')

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')
    filter_horizontal = ('relatives', 'physicians')
    fieldsets = (
            ('Vital Status', {
                'fields': ('vital_status', 'died_on', 'discharged_on')
                }),
            ('Patient Profile', {
                'fields': (
                    'photo',
                    'first_name',
                    'middle_name',
                    'last_name',
                    'gender',
                    'osca_id',
                    'address',
                    'birth_date',
                    'birth_place',
                    'nationality',
                    'civil_status',
                    'most_recent_occupation',
                    'admission_date',
                    'admission_time',
                    'religion',
                    'reminders',
                    'advanced_directives',
                    'admitting_diagnosis',
                    'room_number',
                    'diet',
                    'weight',
                    'height',
                    )
                }),
            ('Contact Person(s)', {
                'fields': ('relatives', 'physicians')
                })
            )

@admin.register(PerformanceAppraisal)
class PerformanceAppraisalAdmin(admin.ModelAdmin):
    pass

@admin.register(EmploymentStatus)
class EmploymentStatusAdmin(admin.ModelAdmin):
    list_display = ('employee', 'employment_status', 'date_started', 'date_due')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass
