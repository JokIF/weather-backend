from django.urls import path
from rest_framework.routers import SimpleRouter

from authen.views.tg_owner import OwnerViewSet


app_name = "authen"

router = SimpleRouter()
router.register("owners", OwnerViewSet, "owners")

urlpatterns = router.urls