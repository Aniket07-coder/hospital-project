from django.contrib import admin
from .models import Doctor, Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor', 'date', 'status')

    actions = ['accept_appointment', 'reject_appointment']

    def accept_appointment(self, request, queryset):
        queryset.update(status='Accepted')

    def reject_appointment(self, request, queryset):
        queryset.update(status='Rejected')


admin.site.register(Doctor)
admin.site.register(Appointment, AppointmentAdmin)