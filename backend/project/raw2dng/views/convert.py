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

def background_convert(image):
    os.system("docker run -v {folder}:/process valentinrudloff/raw2dng /process/{input_path} -o {output_image_file}".format(folder=MEDIA_ROOT, input_path=image.source.name, output_image_file=image.source.name.replace('.ARW', '.dng')))
    image.converted = True
    path = Path(image.source.path.replace('.ARW', '.dng'))
    with path.open(mode='rb') as f:
        image.converted_source = File(f, name=path.name)
        image.save()


@csrf_exempt
def convert(request, id):
    if not Image.objects.filter(pk=id).exists():
        return JsonResponse({'message':'Converted image not found','error':'Image not found use command POST /api/v1/images/' + str(id) + ' to upload an image to convert'}, status=404)
    
    image = Image.objects.get(pk=id)
    if request.method == 'POST':
        if image.converted:
            return JsonResponse({'message':'Image already converted','error':'Image already converted use command GET /api/v1/images/' + str(id) + '/convert to download the converted image'}, status=400)
        threading.Thread(target=background_convert, name="convert", args=[image]).start()
    
    elif request.method == 'GET':
        if not image.converted:
            return JsonResponse({'message':'Image not converted','error':'Image not converted use command POST /api/v1/images/' + str(id) + '/convert to convert the image'}, status=404)
        return FileResponse(image.converted_source.open(), as_attachment=True, filename="output.dng")
    
    return JsonResponse({'message':'Image already converted','error':'Image already converted use command GET /api/v1/images/' + str(id) + '/convert to download the converted image'}, status=400)