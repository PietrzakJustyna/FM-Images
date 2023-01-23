from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image as PILImage


class Image(models.Model):
    title = models.CharField(max_length=255)
    width = models.PositiveIntegerField(validators=[MaxValueValidator(1024)])  # pixels
    height = models.PositiveIntegerField(validators=[MaxValueValidator(1024)])  # pixels
    image_file = models.ImageField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = PILImage.open(self.image_file.path)
        image = image.resize((self.width, self.height))
        image.save(self.image_file.path)

    def __str__(self):
        return self.title
