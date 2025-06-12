# lacrei_saude_api/core_api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthProfessionalViewSet, MedicalAppointmentViewSet

router = DefaultRouter()
router.register(r'healthprofessionals', HealthProfessionalViewSet)
router.register(r'medicalappointments', MedicalAppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]