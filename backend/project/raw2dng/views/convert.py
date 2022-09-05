from pathlib import Path
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.core.files import File
import threading
import mimetypes
mimetypes.init()

from project.settings import MEDIA_ROOT
import os

from raw2dng.serializers.image import ImageSerializer
from raw2dng.models.image import Image, ConvertedImage

class ConvertView(viewsets.ModelViewSet):
    serializer_class = ImageSerializer

    def get_queryset(self):
        user = self.request.GET.get('user')
        queryset = Image.objects.all()
        if user is not None:
            queryset = queryset.filter(user=user)
        return queryset

def function_that_downloads(image):
    #import subprocess
    #subprocess.Popen(["docker run -v {folder}:/process valentinrudloff/raw2dng /process/{input_path} -o {output_image_file}".format(folder=MEDIA_ROOT, input_path=image.source.path, output_image_file=image.source.name.replace('.ARW', '.dng'))], shell=True)
    os.system("docker run -v {folder}:/process valentinrudloff/raw2dng /process/{input_path} -o {output_image_file}".format(folder=MEDIA_ROOT, input_path=image.source.name, output_image_file=image.source.name.replace('.ARW', '.dng')))
    image.converted = True
    path = Path(image.source.path.replace('.ARW', '.dng'))
    with path.open(mode='rb') as f:
        image.converted_source = File(f, name=path.name)
        image.save()


@csrf_exempt
def convert(request, id):
    image = Image.objects.get(pk=id)
    if request.method == 'POST':
        if image.converted:
            return JsonResponse({'message':'Image already converted','error':'Image already converted use command GET /api/v1/images/' + str(id) + '/convert to download the converted image'}, status=400)
        threading.Thread(target=function_that_downloads, name="Downloader", args=[image]).start()
    elif request.method == 'GET':
        print('download converted image if exists')
        if image.converted:
            return FileResponse(image.converted_source.open(), as_attachment=True, filename="output.png")
        else:
            return JsonResponse({'message':'Image not converted','error':'Image not converted use command POST /api/v1/images/' + str(id) + '/convert to convert the image'}, status=404)
    return JsonResponse({'message':'Image already converted','error':'Image already converted use command GET /api/v1/images/' + str(id) + '/convert to download the converted image'}, status=400)