from django.urls import path
from .views import *


urlpatterns = [
    path('', MunicipalityView.as_view({'get': 'list', 'post': 'create'})),
]
