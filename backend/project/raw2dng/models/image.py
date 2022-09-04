from django.core.exceptions import ValidationError
from distutils import extension
from django.db import models
import os
import mimetypes
mimetypes.init()

class ConvertedImage(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=120)
    source = models.FileField(blank=True)

    def save(self, *args, **kwargs):
        print("save")
        #if self.is_valid(source)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.source.delete()
        self.converted_source.delete()
        super().delete(*args, **kwargs)
    
    def convert(self):
        self.converted

    def _str_(self):
        return self.name

    def is_valid(self, image) -> bool:
        mimestart = mimetypes.guess_type(image)[0]
        ext = mimetypes.guess_extension(image)
        print(ext)

        if mimestart and ext:
            mimestart = mimestart.split('/')[0]

            if mimestart  == 'image' and ext in ['nef', 'arw']:
                return True
        
        return False

class Image(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=120)
    source = models.FileField()
    converted = models.BooleanField(blank=True, default=False)
    converted_source = models.FileField(blank=True)

    def save(self, *args, **kwargs):
        print("save")
        #if self.is_valid(source)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.source.delete()
        self.converted_source.delete()
        super().delete(*args, **kwargs)
    
    def convert(self):
        self.converted

    def _str_(self):
        return self.name

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        image = str(self.source)
        mimestart = mimetypes.guess_type(image)[0]
        ext = mimetypes.guess_extension(image)
        print(ext)

        if mimestart and ext:
            mimestart = mimestart.split('/')[0]

            if mimestart != 'image' and ext not in ['nef', 'arw']:
                raise ValidationError(
                    _('Draft entries may not have a publication date.')
                )