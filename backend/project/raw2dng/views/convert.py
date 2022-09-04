from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt

from project.settings import MEDIA_ROOT
import os

from raw2dng.serializers.raw_image import RawImageSerializer
from raw2dng.models.raw_image import RawImage

class ConvertView(viewsets.ModelViewSet):
    serializer_class = RawImageSerializer

    def get_queryset(self):
        user = self.request.GET.get('user')
        queryset = RawImage.objects.all()
        if user is not None:
            queryset = queryset.filter(user=user)
        return queryset

@csrf_exempt
def convert(request, id):
    if request.method == 'POST':
        raw_to_convert = RawImage.objects.get(pk=id)
        print('convert ' + str(raw_to_convert))
        print(MEDIA_ROOT)
        os.system("docker run -v {folder}:/process valentinrudloff/raw2dng /process/{image_file}.ARW -o {image_file}.dng".format(folder=MEDIA_ROOT, image_file='DSC04241'))
    return redirect('/api/v1/raws/'+str(id))