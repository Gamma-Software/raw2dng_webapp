from django.shortcuts import render
from rest_framework import viewsets

from raw2dng.serializers.raw_image import RawImageSerializer
from raw2dng.models.raw_image import RawImage
class RawImageView(viewsets.ModelViewSet):
    serializer_class = RawImageSerializer

    def get_queryset(self):
        user = self.request.GET.get('user')
        queryset = RawImage.objects.all()
        if user is not None:
            queryset = queryset.filter(user=user)
        return queryset
