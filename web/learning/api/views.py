# DRF
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from learning.models import LearningResource, LearningUnit

from .serializers import LearningResourceSerializer, LearningUnitSerializer


class LearningResourceViewSet(viewsets.ModelViewSet):
    queryset = LearningResource.objects.all()
    serializer_class = LearningResourceSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]


class LearningUnitViewSet(viewsets.ModelViewSet):
    queryset = LearningUnit.objects.all()
    serializer_class = LearningUnitSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
