from rest_framework import serializers
from .models import Material


class MaterialSerializers(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ["idProduct", "title", "name", "img", "brand",
                  "price", "screenSize", "memoryCard", "cpu", "videoCard"]
