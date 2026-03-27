from django.urls import path
from sights.views import index
from sights.apps import SightsConfig

app_name = SightsConfig.name

urlpatterns = [
    path('', index, name='index'),
]
