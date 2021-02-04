from rest_framework import serializers
from core import models


class LaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Laboratory
        fields = ('id', 'name', 'latitude', 'longitude', 'has_covid_tests')
        extra_kwargs = {'id': {'read_only': True}}

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hospital
        fields = ('id', 'name', 'latitude', 'longitude', 'has_vaccine',
                  'infected_number')
        extra_kwargs = {'id': {'read_only': True}}
