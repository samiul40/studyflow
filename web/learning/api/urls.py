# DRF
from rest_framework import routers

from .views import LearningResourceViewSet, LearningUnitViewSet

router = routers.DefaultRouter()

router.register("resources", LearningResourceViewSet, basename="resources")
router.register("units", LearningUnitViewSet, basename="units")

urlpatterns = router.urls
