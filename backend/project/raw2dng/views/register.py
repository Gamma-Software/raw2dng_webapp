from http.client import HTTPResponse
from django.contrib.auth.models import User
from raw2dng.serializers.user import RegisterSerializer
from rest_framework import generics
from raw2dng.serializers.user import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def put(self, request, *args, **kwargs):
        username = kwargs.get("username", None)
        if not username:
            return HttpResponseBadRequest("The command is not recognized, POST /api/ to get more info")

        if str(request.user) != username:
            return HttpResponseNotFound("The user you want to update is not not yours")

        try:
            instance = User.objects.get(username=username)
        except Exception:
            return HttpResponseNotFound("User not found")

        serializer = RegisterSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=201)

    def delete(self, request, *args, **kwargs):
        username = kwargs.get("username", None)
        if not username:
            return HttpResponseBadRequest("The command is not recognized, POST /api/ to get more info")

        if str(request.user) != username:
            return HttpResponseNotFound("The user you want to update is not not yours")

        try:
            instance = User.objects.get(username=username)
            instance.delete()
        except Exception:
            return HttpResponseNotFound("User not found")

        return JsonResponse({'message':'User deleted','error':'The user ' + str(username) + ' is deleted'}, status=200)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer