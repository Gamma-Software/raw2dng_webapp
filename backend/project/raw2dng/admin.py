from django.contrib import admin
from raw2dng.models.image import Image

class Admin(admin.ModelAdmin):
    list_display = ['source']
    readonly_fields = ["converted", "converted_source"]

# Register your models here.

admin.site.register(Image, Admin)