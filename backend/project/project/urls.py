"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from raw2dng.views.register import MyObtainTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView
from raw2dng.views import convert, views, image, register

router = routers.DefaultRouter()
router.register(r'images', image.ImageView, 'images')

urlpatterns = [
    path('api/', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('api/v1/api-auth/', include('rest_framework.urls')),
    path('api/v1/login/', MyObtainTokenPairView.as_view(), name='auth_register'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/register/', register.RegisterView.as_view(), name='auth_register'),
    path('api/v1/register/<slug:username>/', register.RegisterView.as_view(), name='auth_register'),
    path('api/v1/', include(router.urls)),
    path('api/v1/images/<int:id>/convert', convert.convert, name='convert'),
    path('api/v1/images/convert', convert.convert_all, name='convert_all'),
]

# Show images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)