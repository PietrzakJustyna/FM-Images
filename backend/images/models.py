from django.db import models
from PIL import Image as PILImage


class Image(models.Model):
    title = models.CharField(max_length=255)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    image_file = models.ImageField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = PILImage.open(self.image_file.path)
        image = image.resize((self.width, self.height))
        image.save(self.image_file.path)
