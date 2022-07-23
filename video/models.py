from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.


class Video(models.Model):
    title = models.TextField(blank=False)
    video = models.FileField(upload_to="videos", blank=False, validators=[
                             FileExtensionValidator(['mp4', "mkv"])])
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
