# lacrei_saude_api/core_api/views.py

from rest_framework import viewsets
from .models import HealthProfessional, MedicalAppointment
from .serializers import HealthProfessionalSerializer, MedicalAppointmentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class HealthProfessionalViewSet(viewsets.ModelViewSet):
    queryset = HealthProfessional.objects.all()
    serializer_class = HealthProfessionalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MedicalAppointmentViewSet(viewsets.ModelViewSet):
    queryset = MedicalAppointment.objects.all()
    serializer_class = MedicalAppointmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        professional_id = self.request.query_params.get('professional_id')
        if professional_id is not None:
            queryset = queryset.filter(health_professional_id=professional_id)
        return queryset