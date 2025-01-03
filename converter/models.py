from django.db import models

# Create your models here.
class Image(models.Model):
    image_file = models.ImageField(upload_to='images')
    @classmethod
    def create(cls,image_file):
       image = cls(image_file=image_file)
       return image

    def __str__(self):
       return f"{self.id}{self.image_file}"
    