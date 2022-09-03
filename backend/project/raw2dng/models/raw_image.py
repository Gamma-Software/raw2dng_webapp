from django.db import models
import os
import mimetypes
mimetypes.init()

# Create your models here.

class RawImage(models.Model):
    name = models.CharField(max_length=120)
    source = models.FileField()
    completed = models.BooleanField(default=False)

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