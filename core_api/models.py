from django.db import models

class HealthProfessional(models.Model):
    social_name = models.CharField(max_length=255)
    profession = models.CharField(unique=False)
    # Address information
    address_street = models.CharField(max_length=100, blank=True, null=True)
    address_number = models.CharField(max_length=10, blank=True, null=True)
    address_city = models.CharField(max_length=50, blank=True, null=True)
    address_state = models.CharField(max_length=30, blank=True, null=True)
    address_zip = models.CharField(max_length=15, blank=True, null=True)
    # Contact information
    contact_email = models.EmailField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.social_name
    
class MedicalAppointment(models.Model):
    health_professional = models.ForeignKey(HealthProfessional, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()

    def __str__(self):
        return f"{self.health_professional} - {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"