from django.urls import path
from GisMeteoImage.views import GismeteoImageViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"weather", GismeteoImageViewSet, basename="weather_image")
app_name = "weather_gism"

urlpatterns = router.urls