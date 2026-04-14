from django.urls import path
from sights.views import index, SightsListView, sight_detail, SightsCreateView, sights_update_view, sights_delete_view, \
    category_list, category_detail, category_create_view
from sights.apps import SightsConfig

app_name = SightsConfig.name

urlpatterns = [
    path('', index, name='index'),
    # sights
    path('sights/', SightsListView.as_view(), name='sight_list'),
    path('sights/<int:pk>/', sight_detail, name='sight_detail'),
    path('sights/create/', SightsCreateView.as_view(), name='sight_create'),
    path('sights/update/<int:pk>/', sights_update_view, name='sights_update'),
    path('sights/delete/<int:pk>/', sights_delete_view, name='sights_delete'),

    # category
    path('category/create/', category_create_view, name='category_create'),
    path('category/', category_list, name='category_list'),
    path('category/<int:pk>/', category_detail, name='category'),

]
