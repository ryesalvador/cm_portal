from django.contrib import admin
from .models import Relative, Physician, Resident, PerformanceAppraisal, \
     EmploymentStatus, Employee, Position, Department, MedicalAbstract, \
     Drug, Medication, Item, MedicalSupply, MedicalEquipment, ResidentWeight

@admin.register(ResidentWeight)
class ResidentWeight(admin.ModelAdmin):
    pass

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass

@admin.register(MedicalSupply)
class MedicalSupplyAdmin(admin.ModelAdmin):
    pass

@admin.register(MedicalEquipment)
class MedicalEquipmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('generic_name', 'brand_name')

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    raw_id_fields = ('medicine',)

@admin.register(MedicalAbstract)
class MedicalAbstractAdmin(admin.ModelAdmin):
    pass

@admin.register(Relative)
class RelativeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'telephone')
    search_fields = ('first_name', 'last_name')
    
@admin.register(Physician)
class PhysicianAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'telephone')
    search_fields = ('first_name', 'last_name')

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')
    filter_horizontal = ('physicians',)
    fieldsets = (
            ('Vital Status', {
                'fields': ('vital_status', 'died_on', 'discharged_on')
                }),
            ('Resident Profile', {
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
                'fields': ('physicians',)
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
