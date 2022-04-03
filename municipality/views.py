from django.shortcuts import render
from rest_framework import viewsets
from .models import Municipality
from .serializers import MunicipalitySerializer


class MunicipalityView(viewsets.ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
    pagination_class = None
