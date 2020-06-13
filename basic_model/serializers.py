from rest_framework import serializers
from .models import SheetUpload,ImageUpload

class SheetUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SheetUpload
        fields = '__all__'

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = '__all__'