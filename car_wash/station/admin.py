from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Client, Service, Employee, Appointment

class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employé'

# Étendre l'admin utilisateur pour montrer le lien avec l'employé
class CustomUserAdmin(UserAdmin):
    inlines = (EmployeeInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_employee_role', 'is_staff')
    
    def get_employee_role(self, obj):
        try:
            return obj.employee.get_role_display()
        except:
            return '-'
    get_employee_role.short_description = 'Rôle'

# Désinscrire l'admin utilisateur par défaut
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'license_plate', 'loyalty_status', 'last_visit')
    list_filter = ('loyalty_status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'license_plate')
    date_hierarchy = 'created_at'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'phone', 'hire_date', 'is_active', 'user')
    list_filter = ('role', 'is_active', 'hire_date')
    search_fields = ('name', 'email', 'phone')
    date_hierarchy = 'hire_date'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'employee', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'service')
    search_fields = ('client__name', 'service__name', 'employee__name')
    date_hierarchy = 'date'