from rest_framework import serializers
from core import models
from math import sin, cos, sqrt, atan2, radians


def calculate_distance(lat1_: float, lon1_: float, lat2_: float, lon2_: float):
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(lat1_)
    lon1 = radians(lon1_)
    lat2 = radians(lat2_)
    lon2 = radians(lon2_)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    # returns distance in KM
    return distance


class LaboratorySerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField(read_only=True)

    def get_distance(self, instance):
        user_lat = self.context['request'].query_params.get('latitude', 0)
        user_lon = self.context['request'].query_params.get('longitude', 0)
        return calculate_distance(instance.latitude, instance.longitude,
                                  float(user_lat), float(user_lon))

    class Meta:
        model = models.Laboratory
        fields = ('id', 'name', 'latitude', 'longitude', 'has_covid_tests',
                  'distance')
        extra_kwargs = {'id': {'read_only': True}}

class HospitalSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField(read_only=True)

    def get_distance(self, instance):
        user_lat = self.context['request'].query_params.get('latitude', 0)
        user_lon = self.context['request'].query_params.get('longitude', 0)
        return calculate_distance(instance.latitude, instance.longitude,
                                  float(user_lat), float(user_lon))
    class Meta:
        model = models.Hospital
        fields = ('id', 'name', 'latitude', 'longitude', 'has_vaccine',
                  'infected_number', 'distance')
        extra_kwargs = {'id': {'read_only': True},
                        'distance': {'read_only': True}}
