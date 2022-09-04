from django.db import models
import os
import mimetypes
mimetypes.init()

# Create your models here.

class RawImage(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    source = models.FileField(blank=True)

    def save(self, *args, **kwargs):
        print("save")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.source.delete()
        super().delete(*args, **kwargs)

    def _str_(self):
        return self.name

    def valid(image) -> bool:
        mimestart = mimetypes.guess_type(image)[0]
        ext = mimetypes.guess_extension(image)
        print(ext)

        if mimestart and ext:
            mimestart = mimestart.split('/')[0]

            if mimestart  == 'image' and ext in ['nef', 'arw']:
                return True
        
        return False