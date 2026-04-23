from django.urls import path
from sights.views import index, SightsListView, SightsDetailView, SightsCreateView, SightsUpdateView, SightsDeleteView, \
    CategoryListView, CategoryDetailView, CategoryCreateView, AddPhotoView, DeletePhotoView
from sights.apps import SightsConfig
from django.views.decorators.cache import cache_page, never_cache

app_name = SightsConfig.name

urlpatterns = [
    path('', cache_page(60)(index), name='index'),
    # sights
    path('sights/', cache_page(60)(SightsListView.as_view()), name='sight_list'),
    path('sights/<int:pk>/', SightsDetailView.as_view(), name='sight_detail'),
    path('sights/create/', never_cache(SightsCreateView.as_view()), name='sight_create'),
    path('sights/update/<int:pk>/', never_cache(SightsUpdateView.as_view()), name='sights_update'),
    path('sights/delete/<int:pk>/', SightsDeleteView.as_view(), name='sights_delete'),

    # gallery
    path('sights/<int:pk>/add-photo/', AddPhotoView.as_view(), name='add_photo'),
    path('sights/photo/delete/<int:pk>/', DeletePhotoView.as_view(), name='delete_photo'),

    # category
    path('category/create/', never_cache(CategoryCreateView.as_view()), name='category_create'),
    path('category/', cache_page(60)(CategoryListView.as_view()), name='category_list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category'),
]
