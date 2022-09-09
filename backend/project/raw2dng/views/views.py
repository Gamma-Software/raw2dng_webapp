from django.http import JsonResponse


def index(request):
    response = {
        "commands": [{
            "images": "GET /api/v1/images/",
            "post one image": "POST /api/v1/images/",
            "one image with id": "GET /api/v1/images/:id/",
            "convert image": "POST /api/v1/images/:id/convert/",
            "download converted image": "GET /api/v1/images/:id/convert/",
        }]
    }
    return JsonResponse(response, status=200)