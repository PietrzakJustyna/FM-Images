import os
import uuid
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.db import models
from PIL import Image as PILImage

ALLOWED_EXT_TO_FORMAT_MAPPING = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "bmp": "BMP",
}


def get_file_path(_, filename):
    name, ext = filename.split(".", 1)
    filename = f"{name}_{uuid.uuid1()}.{ext}"
    return os.path.join("uploaded_images", filename)


class Image(models.Model):
    title = models.CharField(max_length=255)
    width = models.PositiveIntegerField(validators=[MaxValueValidator(1024)])  # pixels
    height = models.PositiveIntegerField(validators=[MaxValueValidator(1024)])  # pixels
    image_file = models.ImageField(
        upload_to=get_file_path,
        validators=[FileExtensionValidator(ALLOWED_EXT_TO_FORMAT_MAPPING.keys())],
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._resize_image()

    def _resize_image(self):
        with default_storage.open(self.image_file.name, "rb") as image_file:
            with PILImage.open(image_file) as im, BytesIO() as resized_image:
                ext = image_file.name.split(".")[-1].lower()
                im = im.resize((self.width, self.height))
                im.save(resized_image, format=ALLOWED_EXT_TO_FORMAT_MAPPING[ext])
                resized_image.seek(0)
                default_storage.save(
                    self.image_file.name, ContentFile(resized_image.read())
                )

    def __str__(self):
        return self.title
