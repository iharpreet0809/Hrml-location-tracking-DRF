from django.contrib import admin
from django.contrib.auth.models import User
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_employee_info', 'latitude', 'longitude', 'accuracy', 'formatted_timestamp']
    list_filter = ['employee', 'timestamp']
    search_fields = ['employee__username', 'employee__first_name', 'employee__last_name']
    readonly_fields = ['timestamp', 'employee']
    ordering = ['-timestamp']
    list_per_page = 50
    date_hierarchy = 'timestamp'
    
    def get_employee_info(self, obj):
        """Display employee username and ID"""
        return f"{obj.employee.username} (ID: {obj.employee.id})"
    get_employee_info.short_description = 'Employee'
    get_employee_info.admin_order_field = 'employee__username'
    
    def formatted_timestamp(self, obj):
        """Display formatted timestamp"""
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    formatted_timestamp.short_description = 'Tracked At'
    formatted_timestamp.admin_order_field = 'timestamp'
    
    def has_add_permission(self, request):
        """Prevent manual addition of locations from admin"""
        return False
    
    def get_queryset(self, request):
        """Optimize query with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('employee')
