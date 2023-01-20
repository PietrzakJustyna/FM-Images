from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=255)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    image_file = models.ImageField()
