from django.urls import path
from sights.views import index, sight_list, sight_detail, sight_create_view, category_list, category_detail
from sights.apps import SightsConfig

app_name = SightsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('sights/', sight_list, name='sight_list'),
    path('sights/<int:pk>/sight_detail/', sight_detail, name='sight_detail'),
    path('sights/create/', sight_create_view, name='sight_create'),
    path('category/', category_list, name='category_list'),
    path('category/<int:pk>/', category_detail, name='category'),
]
