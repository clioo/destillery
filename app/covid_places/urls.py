from django.urls import path
from rest_framework.routers import SimpleRouter
from covid_places import views


router = SimpleRouter()
router.register('laboratories', views.LaboratoryViewSet, 'laboratories')
router.register('hospitals', views.HospitalViewSet, 'hospitals')
app_name = 'covid_places'


urlpatterns = []
urlpatterns += router.urls
