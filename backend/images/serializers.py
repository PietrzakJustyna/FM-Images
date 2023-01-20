from images.models import Image
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField("get_image_url")

    def get_image_url(self, obj):
        return obj.image_file.url

    class Meta:
        model = Image
        fields = ("id", "title", "height", "width", "url")
