from django.http import JsonResponse


def index(request):
    response = {
        "commands": [{
            "register a user": "GET api/v1/register/",
            "update a user": "PUT api/v1/register/:username",
            "login": "GET api/v1/login/",
            "refresh the token": "GET api/v1/token/refresh",
            "images": "GET /api/v1/images/",
            "post one image": "POST /api/v1/images/",
            "one image with id": "GET /api/v1/images/:id/",
            "convert image": "POST /api/v1/images/:id/convert/",
            "convert all user images": "POST /api/v1/images/convert/",
            "download converted image": "GET /api/v1/images/:id/convert/",
        }]
    }
    return JsonResponse(response, status=200)