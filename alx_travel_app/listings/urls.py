from django.urls import path, include, re_path

from .views import ListingViewSet

urlpatterns = [

    path('', ListingViewSet.as_view(), name='listing-list'),
]
