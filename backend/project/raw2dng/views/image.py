from django.shortcuts import render
from rest_framework import viewsets

from raw2dng.serializers.image import ImageSerializer
from raw2dng.models.image import Image

class ImageView(viewsets.ModelViewSet):
    serializer_class = ImageSerializer

    def get_queryset(self):
        user = self.request.GET.get('user')
        queryset = Image.objects.all()
        if user is not None:
            queryset = queryset.filter(user=user)
        return queryset
        
    # def get(self, *args, **kwargs):
    #     categories = Category.objects.all()
    #     serializer = CategorySerializer(categories, many=True)
    #     return Response(serializer.data)
