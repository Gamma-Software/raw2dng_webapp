import json
from django.core import serializers
from rest_framework import viewsets
from raw2dng.views.permission import IsUserAuthenticated
from django.http import JsonResponse, HttpResponseNotFound, Http404

from raw2dng.serializers.image import ImageSerializer
from raw2dng.models.image import Image

class ImageView(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [IsUserAuthenticated]

    def create(self, request, *args, **kwargs):
        new_image = Image.objects.create(user=str(request.user), source=request.data["source"])
        new_image.save()
        # return JsonResponse(serializers.serialize('json', [new_image]), safe = False)
        j = json.loads(serializers.serialize('json', [new_image]))
        id = j[0]['pk']
        result = [{"id": id}]
        for key, value in j[0]['fields'].items():
            result[0][key] = value
        return JsonResponse(result, safe=False,  status=201)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            id = json.loads(serializers.serialize('json', [instance]))[0]["pk"]
            self.perform_destroy(instance)
            return JsonResponse({"message": "Image successfully deleted", "success": "Image "+ str(id) +" successfully deleted"},  status=201)
        except Http404:
            return HttpResponseNotFound("Not found")
    
    def get_queryset(self):
        queryset = Image.objects.all()
        if self.request.user is not None:
            queryset = queryset.filter(user=self.request.user)
        return queryset
            
