from django.urls import path
from sights.views import index, sight_list, sight_detail
from sights.apps import SightsConfig

app_name = SightsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('sights/', sight_list, name='sight'),
    path('sights/<int:pk>/sight_detail/',sight_detail, name='sight_detail'),
]
