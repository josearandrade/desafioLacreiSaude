# lacrei_saude_api/core_api/tests.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import HealthProfessional, MedicalAppointment
from datetime import datetime
from django.utils import timezone

User = get_user_model()

class HealthProfessionalAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.list_url = reverse('healthprofessional-list')
        
        self.professional_data = {
            "social_name": "Dr. João Teste",
            "profession": "Clínico Geral",
            "address_street": "Rua A",
            "address_number": "100",
            "address_city": "Cidade Teste",
            "address_state": "SP",
            "address_zip": "00000-000",
            "contact_email": "joao@teste.com",
            "contact_phone": "11912345678"
        }

        self.professional = HealthProfessional.objects.create(
            social_name=self.professional_data['social_name'],
            profession=self.professional_data['profession'],
            address_street=self.professional_data['address_street'],
            address_number=self.professional_data['address_number'],
            address_city=self.professional_data['address_city'],
            address_state=self.professional_data['address_state'],
            address_zip=self.professional_data['address_zip'],
            contact_email=self.professional_data['contact_email'],
            contact_phone=self.professional_data['contact_phone']
        )
        self.detail_url = reverse('healthprofessional-detail', kwargs={'pk': self.professional.id})


    def test_list_health_professionals(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_health_professional(self):
        response = self.client.post(self.list_url, self.professional_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HealthProfessional.objects.count(), 2)

    def test_create_health_professional_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(self.list_url, self.professional_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_health_professional(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['social_name'], self.professional_data['social_name'])

    def test_update_health_professional(self):
        updated_data = self.professional_data.copy()
        updated_data['social_name'] = "Dra. Maria Atualizada"
        updated_data['profession'] = "Cardiologista"
        updated_data['address_state'] = "RJ"      
        updated_data['contact_phone'] = "21987654321" 
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.professional.refresh_from_db()
        self.assertEqual(self.professional.social_name, "Dra. Maria Atualizada")
        self.assertEqual(self.professional.profession, "Cardiologista") 
        self.assertEqual(self.professional.address_state, "RJ")         
        self.assertEqual(self.professional.contact_phone, "21987654321")



    def test_update_health_professional_unauthenticated(self):
        self.client.credentials()
        updated_data = self.professional_data.copy()
        updated_data['social_name'] = "Dra. Maria Atualizada"
        updated_data['profession'] = "Pediatra"
        updated_data['address_state'] = "MG"
        updated_data['contact_phone'] = "31912345678"
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_health_professional(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HealthProfessional.objects.count(), 0)

    def test_delete_health_professional_unauthenticated(self):
        self.client.credentials()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MedicalAppointmentAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='testpassword2')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.list_url = reverse('medicalappointment-list')

        self.professional1 = HealthProfessional.objects.create(
            social_name="Prof Teste 1", profession="Cardiologista",
            address_city="Cidade A", contact_email="a@test.com",
            address_street="Rua C", address_number="1", address_state="SP", address_zip="12345-000", contact_phone="111111111"
        )
        self.professional2 = HealthProfessional.objects.create(
            social_name="Prof Teste 2", profession="Pediatra",
            address_city="Cidade B", contact_email="b@test.com",
            address_street="Rua D", address_number="2", address_state="RJ", address_zip="54321-000", contact_phone="222222222"
        )
        
        self.appointment1 = MedicalAppointment.objects.create(
            health_professional=self.professional1,
            appointment_date=timezone.now() + timezone.timedelta(days=1)
        )
        self.appointment2 = MedicalAppointment.objects.create(
            health_professional=self.professional1,
            appointment_date=timezone.now() + timezone.timedelta(days=2)
        )
        self.appointment3 = MedicalAppointment.objects.create(
            health_professional=self.professional2,
            appointment_date=timezone.now() + timezone.timedelta(days=3)
        )
        self.detail_url = reverse('medicalappointment-detail', kwargs={'pk': self.appointment1.id})

    def test_list_medical_appointments(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_medical_appointment(self):
        new_appointment_data = {
            'health_professional_id': self.professional2.id,
            'appointment_date': (timezone.now() + timezone.timedelta(days=10)).isoformat()
        }
        response = self.client.post(self.list_url, new_appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicalAppointment.objects.count(), 4)

    def test_create_medical_appointment_unauthenticated(self):
        self.client.credentials()
        new_appointment_data = {
            'health_professional_id': self.professional2.id,
            'appointment_date': (timezone.now() + timezone.timedelta(days=10)).isoformat()
        }
        response = self.client.post(self.list_url, new_appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_retrieve_medical_appointment(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.appointment1.id)
        self.assertIn('health_professional', response.data)
        self.assertEqual(response.data['health_professional']['id'], self.professional1.id)

    def test_update_medical_appointment(self):
        updated_date = timezone.now() + timezone.timedelta(days=5)
        updated_data = {
            'health_professional_id': self.professional2.id,
            'appointment_date': updated_date.isoformat()
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment1.refresh_from_db()
        self.assertEqual(self.appointment1.health_professional, self.professional2)
        self.assertAlmostEqual(self.appointment1.appointment_date, updated_date, delta=timezone.timedelta(seconds=1))

    def test_update_medical_appointment_unauthenticated(self):
        self.client.credentials()
        updated_date = timezone.now() + timezone.timedelta(days=5)
        updated_data = {
            'health_professional_id': self.professional2.id,
            'appointment_date': updated_date.isoformat()
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_medical_appointment(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MedicalAppointment.objects.count(), 2)

    def test_delete_medical_appointment_unauthenticated(self):
        self.client.credentials()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_medical_appointments_by_professional_id(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        search_url_prof1 = f"{self.list_url}?professional_id={self.professional1.id}"
        response = self.client.get(search_url_prof1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for appointment in response.data:
            self.assertEqual(appointment['health_professional']['id'], self.professional1.id)

        search_url_prof2 = f"{self.list_url}?professional_id={self.professional2.id}"
        response = self.client.get(search_url_prof2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['health_professional']['id'], self.professional2.id)

        search_url_nonexistent = f"{self.list_url}?professional_id=99999"
        response = self.client.get(search_url_nonexistent)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)