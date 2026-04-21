from django.urls import path

from reviews.apps import ReviewsConfig
from reviews.views import ReviewListView, ReviewDeactivatedListView, ReviewCreateView, ReviewDetailView, \
    ReviewDeleteView, ReviewUpdateView, review_toggle_activity

app_name = ReviewsConfig.name

urlpatterns = [
    path('', ReviewListView.as_view(), name='reviews_list'),
    path('deactivated/', ReviewDeactivatedListView.as_view(), name='reviews_deactivated'),  # Добавьте слэш
    path('create/', ReviewCreateView.as_view(), name='review_create'),  # Изменил на create/
    path('detail/<slug:slug>/', ReviewDetailView.as_view(), name='review_detail'),
    path('update/<slug:slug>/', ReviewUpdateView.as_view(), name='review_update'),
    path('delete/<slug:slug>/', ReviewDeleteView.as_view(), name='review_delete'),
    path('toggle/<slug:slug>/', review_toggle_activity, name='review_toggle'),
]