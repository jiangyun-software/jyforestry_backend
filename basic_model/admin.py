from django.contrib import admin
from .models import ImageUpload,SheetUpload

# Register your models here.
admin.site.register(SheetUpload)
admin.site.register(ImageUpload)