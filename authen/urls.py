from django.urls import path

from authen.views import OwnerViewSet
from authen.routes import OwnerViewRouter


app_name = "authen"

router = OwnerViewRouter()
router.register("owners", OwnerViewSet, "owners")

urlpatterns = router.urls