from rest_framework import viewsets, generics, status
from .serializers import LaboratorySerializer, HospitalSerializer
from django.contrib.gis.geos import Point
from core import models
from django.contrib.gis.db.models.functions import Distance
from rest_framework.response import Response
from django.conf import settings
import re
import geocoder


class BaseLocationViewSet(viewsets.ModelViewSet):

    def perform_create(self, serializer):
        point = Point(serializer.validated_data.get('latitude', 0),
                      serializer.validated_data.get('longitude', 0))
        serializer.save(geolocation=point)

    def perform_update(self, serializer):
        point = Point(serializer.validated_data.get('latitude', 0),
                      serializer.validated_data.get('longitude', 0))
        serializer.save(geolocation=point)

    def get_queryset(self):
        longitude = self.request.query_params.get('longitude', 0)
        latitude = self.request.query_params.get('latitude', 0)
        user_location = Point(float(latitude), float(longitude), srid=4326)
        dataset = self.queryset.annotate(
            distance=Distance('geolocation', user_location)
        ).order_by('distance')
        return dataset


class LaboratoryViewSet(BaseLocationViewSet):
    serializer_class = LaboratorySerializer
    queryset = models.Laboratory.objects.all()


class HospitalViewSet(BaseLocationViewSet):
    serializer_class = HospitalSerializer
    queryset = models.Hospital.objects.all()


class BaseGeocodingRetrieveView(generics.RetrieveAPIView):
    def is_latlng_valid(self, latlng: str) -> bool:
        latlng_regex = r'^(-?\d+(\.\d+)?),(-?\d+(\.\d+)?)$'
        is_match = bool(re.match(latlng_regex, latlng))
        return is_match


class GeocodingView(BaseGeocodingRetrieveView):
    def retrieve(self, request):
        address = self.request.query_params.get('address', '')
        if not address:
            return Response({'message': f'Bad address: {address}.'},
                            status.HTTP_400_BAD_REQUEST)
        g = geocoder.google(address, key=settings.API_KEY)
        return Response(g.json, g.status_code)


class ReverseGeocodingView(BaseGeocodingRetrieveView):
    def retrieve(self, request):
        latlng = self.request.query_params.get('latlng', '0,0')
        if not self.is_latlng_valid(latlng):
            return Response({'message': f'Bad format of latlng: {latlng}.'},
                            status.HTTP_400_BAD_REQUEST)
        latlng = latlng.split(',')
        # making coords floats
        latlng = [float(cord) for cord in latlng]
        g = geocoder.google(latlng, method='reverse',
                            components=f"key:{settings.API_KEY}")
        return Response(g.json, g.status_code)
