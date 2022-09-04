from rest_framework import serializers
from raw2dng.models.raw_image import RawImage

class RawImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawImage
        fields = ('id', 'user', 'date_created', 'name', 'source')