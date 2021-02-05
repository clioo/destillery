from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core import models


HOSPITAL_LIST_URL = reverse('covid_places:hospitals-list')
LABORATORY_LIST_URL = reverse('covid_places:laboratories-list')
GEOCODING_URL = reverse('covid_places:geocoding')
REVERSE_GEOCODING_URL = reverse('covid_places:reverse-geocoding')


def get_hospital_detail_url(hospital_id):
    return reverse('covid_places:hospitals-detail', args=[hospital_id])


def get_laboratory_detail_url(laboratory_id):
    return reverse('covid_places:laboratories-detail', args=[laboratory_id])


class PublicPlacesAPI(TestCase):
    """Testing public API endpoints."""
    def setUp(self):
        self.client = APIClient()

    def test_create_laboratory_success_201(self):
        payload={'name': 'My first lab', 'latitude': 53.0, 'longitude': 0.0}
        self.assertEqual(models.Laboratory.objects.count(), 0)
        res = self.client.post(LABORATORY_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Laboratory.objects.count(), 1)

    def test_update_laboratory_success_200(self):
        payload={'name': 'My first lab', 'latitude': 53.0, 'longitude': 0.0}
        res = self.client.post(LABORATORY_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        id_ = res.data.get('id')
        payload['name'] = 'new name'
        res = self.client.put(get_laboratory_detail_url(id_), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        instance = models.Laboratory.objects.get(pk=id_)
        self.assertEqual(instance.name, payload['name'])

    def test_patch_laboratory_success_204(self):
        payload={'name': 'My first lab', 'latitude': 53.0, 'longitude': 0.0}
        res = self.client.post(LABORATORY_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        id_ = res.data.get('id')
        payload['name'] = 'new name'
        latitude = payload.pop('latitude')
        payload.pop('longitude')
        res = self.client.patch(get_laboratory_detail_url(id_), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        instance = models.Laboratory.objects.get(pk=id_)
        self.assertEqual(instance.name, payload['name'])
        self.assertEqual(instance.latitude, latitude)

    def test_list_laboratory_success_200(self):
        for i in range(3):
            payload={'name': f'My lab number {i}', 'latitude': 53.0, 'longitude': 0.0}
            res = self.client.post(LABORATORY_LIST_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Laboratory.objects.count(), 3)
        res = self.client.get(LABORATORY_LIST_URL)
        self.assertEqual(len(res.data.get('results')), 3)

    def test_detail_laboratory_success_200(self):
        payload={'name': 'My first lab', 'latitude': 53.0, 'longitude': 0.0}
        res = self.client.post(LABORATORY_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        id_ = res.data.get('id')
        detail_url = get_laboratory_detail_url(id_)
        res = self.client.get(detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_laboratory_success_204(self):
        payload={'name': 'My first lab', 'latitude': 53.0, 'longitude': 0.0}
        res = self.client.post(LABORATORY_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        id_ = res.data.get('id')
        detail_url = get_laboratory_detail_url(id_)
        res = self.client.delete(detail_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

class GeocodingAPI(TestCase):
    """Testing public API endpoints."""
    def setUp(self):
        self.client = APIClient()

    def test_reverse_geocoding_base_request_space_404(self):
        res = self.client.get(REVERSE_GEOCODING_URL, {'latlng': '12, a23'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reverse_geocoding_base_request_2_commas_404(self):
        res = self.client.get(REVERSE_GEOCODING_URL, {'latlng': '3.0,3.0,12.0'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reverse_geocoding_base_request_200(self):
        res = self.client.get(REVERSE_GEOCODING_URL, {'latlng': '25.776802366212806,-108.97180816719028'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_geocoding_base_request_404(self):
        res = self.client.get(GEOCODING_URL, {'address': ''})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_geocoding_base_no_params_request_404(self):
        res = self.client.get(GEOCODING_URL)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_geocoding_base_request_200(self):
        res = self.client.get(GEOCODING_URL, {'address': 'galeana 1657 villa owen'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
