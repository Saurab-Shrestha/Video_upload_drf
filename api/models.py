from django.db import models
# Create your models here.
from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator


class Video(models.Model):
    title = models.CharField(max_length=250,blank=True, null=True)
    video_file = models.FileField(upload_to='videos/',help_text="Formats accepted: MP4 and MKV,"
                                                                " Video length cannot exceed 10min,"
                                                                "Video size cannot be more than 1GB",
                                 validators=[FileExtensionValidator(allowed_extensions=['mp4','mkv'])])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('api',kwargs={'pk':self.pk})
