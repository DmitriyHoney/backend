from rest_framework import generics
from .models import AddressInfo
from .serializers import AddressInfoSerializer


class AddressListView(generics.ListCreateAPIView):
    queryset = AddressInfo.objects.all()
    serializer_class = AddressInfoSerializer


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AddressInfo.objects.all()
    serializer_class = AddressInfoSerializer