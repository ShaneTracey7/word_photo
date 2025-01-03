from django.contrib import admin
from converter.models import Image
# Register your models here.
class ImageAdmin(admin.ModelAdmin):
  list_display = ("id","image_file")

admin.site.register(Image, ImageAdmin)