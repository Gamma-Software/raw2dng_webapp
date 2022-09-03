from django.shortcuts import render
from rest_framework import viewsets

from raw2dng.serializers.raw_image import RawImageSerializer
from raw2dng.models.raw_image import RawImage

# Create your views here.

class RawImageView(viewsets.ModelViewSet):
    serializer_class = RawImageSerializer
    queryset = RawImage.objects.all()
    