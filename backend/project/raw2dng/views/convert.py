from pathlib import Path
from django.http import JsonResponse, FileResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.core.files import File
import threading
import concurrent.futures
import os
import docker
import platform

from project.settings import MEDIA_ROOT
from raw2dng.models.image import Image

def background_convert(docker_client, image):
    # os.system("docker run -v {folder}:/process valentinrudloff/raw2dng /process/{input_path} -o {output_image_file}".format(folder=MEDIA_ROOT, input_path=image.source.name, output_image_file=image.source.name.replace('.ARW', '.dng')))
    docker_client.containers.run("valentinrudloff/raw2dng:"+platform.processor(), command="/process/{input_path} -o {output_image_file}".format(folder=MEDIA_ROOT, input_path=image.source.name, output_image_file=image.source.name.replace('.ARW', '.dng'), detach=True))
    # TODO continue after convert depending on its output
    image.converted = True
    path = Path(image.source.path.replace('.ARW', '.dng'))
    with path.open(mode='rb') as f:
        image.converted_source = File(f, name=path.name)
        image.save()


@csrf_exempt
@api_view(["POST", "GET"])
def convert(request, id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("User not authenticated")

    if not Image.objects.filter(pk=id).exists():
        return JsonResponse({'message':'Converted image not found','error':'Image not found use command POST /api/v1/images/' + str(id) + ' to upload an image to convert'}, status=404)
    
    image = Image.objects.get(pk=id)
    if request.method == 'POST':
        docker_client = docker.from_env()
        if image.converted:
            return JsonResponse({'message':'Image already converted','error':'Image already converted use command GET /api/v1/images/' + str(id) + '/convert to download the converted image'}, status=400)
        threading.Thread(target=background_convert, name="convert", args=[docker_client, image]).start()
        return JsonResponse({'message':'Image converting in DNG','success':'Converting in progress use command GET /api/v1/images/' + str(id) + '/convert to download the converted image when convertion finished'}, status=200)
    
    elif request.method == 'GET':
        if not image.converted:
            return JsonResponse({'message':'Image not converted','error':'Image not converted use command POST /api/v1/images/' + str(id) + '/convert to convert the image'}, status=404)
        return FileResponse(image.converted_source.open(), as_attachment=True, filename="output.dng")
    
    return HttpResponseBadRequest("The command is not recognized, POST /api/ to get more info")

@api_view(["POST"])
def convert_all(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("User not authenticated")

    if request.method == 'POST':
        # Get all the images from the user
        queryset = Image.objects.all()
        if request.user is not None:
            queryset = queryset.filter(user=request.user.username, converted='False')
        if not queryset:
            return JsonResponse({'message':'No images to convert from user','error':'No images to convert from user' + str(request.user)}, status=200)
        
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        for image in queryset:
            executor.submit(background_convert, image=image)
        executor.shutdown(wait=False)
        return JsonResponse({'message':'Images converting in DNG','success':f'Converting {queryset} in progress use command GET /api/v1/images/' + str(id) + '/convert to download the converted image when convertion finished'}, status=200)
    
    return HttpResponseBadRequest("The command is not recognized, POST /api/ to get more info")