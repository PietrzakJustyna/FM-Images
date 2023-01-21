import django_filters
from images.models import Image


class ImageTitleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Image
        fields = ["title"]
