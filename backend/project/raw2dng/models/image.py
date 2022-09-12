from django.core.exceptions import ValidationError
from django.db import models
from django.core.files.images import get_image_dimensions



class Image(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=120, blank=True, auto_created=True)
    source = models.FileField()
    converted = models.BooleanField(blank=True, default=False)
    converted_source = models.FileField(blank=True)

    def save(self, *args, **kwargs):
        #if self.is_valid(source)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.source.delete()
        if self.converted:
            self.converted_source.delete()
        super().delete(*args, **kwargs)
    
    def convert(self):
        self.converted

    def _str_(self):
        return self.name