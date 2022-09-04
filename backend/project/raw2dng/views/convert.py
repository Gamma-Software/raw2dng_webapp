from pathlib import Path
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.core.files import File
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
    import subprocess
    print(image.source.path)
    print(image.source.name.replace('.ARW', '.dng'))
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
    if request.method == 'POST' and not image.converted:
        import threading
        convert_thread = threading.Thread(target=function_that_downloads, name="Downloader", args=[image])
        convert_thread.start()
    elif request.method == 'GET':
        print('download converted image if exists')
        if not image.converted:
            return JsonResponse({'message':'error','explanation':'Image not converted'}, status=404)
        else:
            print(image.converted_source.url)
            return redirect(image.converted_source.url)
            filepath = MEDIA_ROOT + '/' + image.source.name.replace('.ARW', '.dng')
            with open(filepath, 'r') as file:
                # Set the mime type
                mime_type, _ = mimetypes.guess_type(filepath)
                # Set the return value of the HttpResponse
                response = HttpResponse(file, content_type=mime_type)
                # Set the HTTP header for sending to browser
                response['Content-Disposition'] = "attachment; filename=%s" % image.source.name.replace('.ARW', '.dng')
                # Return the response value
                return response

    return redirect('/api/v1/images/'+str(id))