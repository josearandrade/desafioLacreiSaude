from django.contrib import admin
from .models import HealthProfessional, MedicalAppointment

# Register your models here.

admin.site.register(HealthProfessional)
admin.site.register(MedicalAppointment)