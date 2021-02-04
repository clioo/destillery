from rest_framework import viewsets
from .serializers import LaboratorySerializer, HospitalSerializer
from django.contrib.gis.geos import Point
from core import models


class BaseLocationViewSet(viewsets.ModelViewSet):

    def perform_create(self, serializer):
        point = Point(serializer.validated_data.get('latitude', 0),
                      serializer.validated_data.get('longitude', 0))
        serializer.save(point=point)
    
    def get_queryset(self):
        # return nearest by given lat and lng in params
        return self.queryset

class LaboratoryViewSet(BaseLocationViewSet):
    serializer_class = LaboratorySerializer
    queryset = models.Laboratory.objects.all()

class HospitalViewSet(BaseLocationViewSet):
    serializer_class = HospitalSerializer
    queryset = models.Hospital.objects.all()
