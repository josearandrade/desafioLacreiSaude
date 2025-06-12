from rest_framework import serializers

from .models import HealthProfessional, MedicalAppointment  # Replace with your actual model(s)

class HealthProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProfessional
        # Inclua todos os novos campos de endereço e contato
        fields = [
            'id',
            'social_name',
            'profession',
            'address_street',
            'address_number',
            'address_city',
            'address_state',
            'address_zip',
            'contact_email',
            'contact_phone'
        ]
        read_only_fields = ['id']

class MedicalAppointmentSerializer(serializers.ModelSerializer):
    health_professional = HealthProfessionalSerializer(read_only=True)
    health_professional_id = serializers.PrimaryKeyRelatedField(
        queryset=HealthProfessional.objects.all(),
        source='health_professional',
        write_only=True                             
    )
    class Meta:
        model = MedicalAppointment
        # Inclua ambos os campos de profissional (aninhado para leitura e ID para escrita)
        fields = ['id', 'appointment_date', 'health_professional', 'health_professional_id']
        read_only_fields = ['id']