from django.db import models
from django.utils import timezone
#from django.core.files.storage import FileSystemStorage

from utils.cloud_storage import upload, delete, IMAGE, VIDEO, DEV_BUCKET


class Image(models.Model):
    name = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )

    url = models.URLField(
        unique=True,
        max_length=512,
        editable=False
    )

    image = models.ImageField(blank=True, null=True)

    uploaded_at = models.DateTimeField(editable=False, null=True)

    labels = models.CharField(
        max_length=512,
        blank=True,
        null=True
    )
    

    def __str__(self):
        if self.name:
            return self.name
        if self.url:
            return self.url.split('/')[-1]
        return str(self.id)
    
    # upload image to google cloud, set the url, and remove image on save (so it doesn't get stored to local)
    def save(self, *args, **kwargs):
        if self.image:
            self.uploaded_at = timezone.now()
            file_path = upload(self.image, DEV_BUCKET, IMAGE)
            self.url = file_path
            self.image = None
            if not self.name:
                self.name = file_path.split('/')[-1]
        super(Image, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-uploaded_at',]
