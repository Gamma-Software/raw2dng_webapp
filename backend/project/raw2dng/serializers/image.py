from rest_framework import serializers
from raw2dng.models.image import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'user', 'date_created', 'source', 'converted', 'converted_source')