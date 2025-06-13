from rest_framework import viewsets

from django.shortcuts import render

from .models import Listing
from .serializers import ListingSerializer


# Create your views here.

class ListingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing listing instances.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned listings to a given user,
        by filtering against a `user_id` query parameter in the URL.
        """
        queryset = self.queryset
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(host_id__user_id=user_id)
        return queryset

    def perform_create(self, serializer):
        """
        Save the listing with the current user as the host.
        """
        serializer.save(host_id=self.request.user)

    def perform_update(self, serializer):
        """
        Update the listing with the current user as the host.
        """
        serializer.save(host_id=self.request.user)
