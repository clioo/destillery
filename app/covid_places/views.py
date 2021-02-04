from rest_framework import viewsets
from .serializers import LaboratorySerializer, HospitalSerializer
from django.contrib.gis.geos import Point
from core import models
from django.contrib.gis.db.models.functions import Distance


class BaseLocationViewSet(viewsets.ModelViewSet):

    def perform_create(self, serializer):
        point = Point(serializer.validated_data.get('latitude', 0),
                      serializer.validated_data.get('longitude', 0))
        serializer.save(point=point)
    
    def get_queryset(self):
        longitude = self.request.query_params.get('longitude', 0)
        latitude= self.request.query_params.get('latitude', 0)
        user_location = Point(latitude, longitude, srid=4326)
        dataset = self.queryset.annotate(
            distance=Distance('point', user_location)
        ).order_by('distance')
        import pdb; pdb.set_trace()
        return self.queryset

class LaboratoryViewSet(BaseLocationViewSet):
    serializer_class = LaboratorySerializer
    queryset = models.Laboratory.objects.all()

class HospitalViewSet(BaseLocationViewSet):
    serializer_class = HospitalSerializer
    queryset = models.Hospital.objects.all()
