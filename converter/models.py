from django.db import models

# Create your models here.
class Image(models.Model):
    image_file = models.ImageField(upload_to='images')
    size = models.CharField(max_length=10, default="medium")
    @classmethod
    def create(cls,image_file,size):
       image = cls(image_file=image_file,size=size)
       return image

    def __str__(self):
       return f"{self.id}{self.image_file}"
    