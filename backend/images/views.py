from images.models import Image
from images.serializers import ImageSerializer
from rest_framework import parsers, viewsets


class ImageViewset(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ["get", "post"]
