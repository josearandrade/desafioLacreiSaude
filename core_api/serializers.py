# lacrei_saude_api/core_api/serializers.py

from rest_framework import serializers
from .models import HealthProfessional, MedicalAppointment
from django.utils import timezone
import re

class HealthProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProfessional
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

        extra_kwargs = {
            'social_name': {'required': True, 'error_messages': {'required': 'O nome social é obrigatório.'}},
            'profession': {'required': True, 'error_messages': {'required': 'A profissão é obrigatória.'}},
            'contact_email': {'required': False},
        }

    def validate_profession(self, value):
        allowed_professions = [
            'Médico(a)', 'Enfermeiro(a)', 'Psicólogo(a)', 'Fisioterapeuta',
            'Nutricionista', 'Dentista', 'Cardiologista', 'Pediatra',
            'Clínico Geral', 'Dermatologista', 'Psiquiatra'
        ]
        if value.strip().lower() not in [p.lower() for p in allowed_professions]:
            raise serializers.ValidationError(
                f"Profissão inválida. As profissões permitidas são: {', '.join(allowed_professions)}."
            )
        return value.strip()

    def validate_address_state(self, value):
        brazilian_states = [
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS',
            'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC',
            'SP', 'SE', 'TO'
        ]
        if value.strip().upper() not in brazilian_states:
            raise serializers.ValidationError(
                f"Estado inválido. Use uma sigla de estado brasileiro (ex: SP, RJ)."
            )
        return value.strip().upper()

    def validate_contact_phone(self, value):
        cleaned_phone = re.sub(r'\D', '', value)

        if not (10 <= len(cleaned_phone) <= 11):
            raise serializers.ValidationError(
                "Número de telefone inválido. Deve ter entre 10 e 11 dígitos, incluindo o DDD."
            )
        return value

class MedicalAppointmentSerializer(serializers.ModelSerializer):
    health_professional = HealthProfessionalSerializer(read_only=True)
    health_professional_id = serializers.PrimaryKeyRelatedField(
        queryset=HealthProfessional.objects.all(),
        source='health_professional',
        write_only=True,
        error_messages={'does_not_exist': 'Profissional de saúde com este ID não existe.'}
    )

    class Meta:
        model = MedicalAppointment
        fields = ['id', 'appointment_date', 'health_professional', 'health_professional_id']
        read_only_fields = ['id']

        extra_kwargs = {
            'appointment_date': {'required': True, 'error_messages': {'required': 'A data da consulta é obrigatória.'}},
            'health_professional_id': {'required': True, 'error_messages': {'required': 'O ID do profissional é obrigatório.'}},
        }

    def validate_appointment_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("A data da consulta não pode ser no passado.")

        return value
