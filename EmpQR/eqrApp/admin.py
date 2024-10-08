from django.contrib import admin
from eqrApp import models

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ('employee_code', 'first_name', 'last_name', 'department', 'position')  # Adjust fields as necessary
    # Specify the fields to filter by
    list_filter = ('department', 'position')  # Adjust fields as necessary

class LogRecordAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ('employee_pk', 'time')  # Adjust fields as necessary
    # Specify the fields to filter by
    # list_filter = ('action')  # Adjust fields as necessary

# Register your models with their respective admin classes
admin.site.register(models.Employee, EmployeeAdmin)
admin.site.register(models.LogRecord, LogRecordAdmin)

