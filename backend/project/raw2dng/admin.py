from django.contrib import admin
from raw2dng.models.raw_image import RawImage

class Admin(admin.ModelAdmin):
    list_display = ('name', 'source')

# Register your models here.

admin.site.register(RawImage, Admin)