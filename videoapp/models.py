from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateField()
    body_text = models.TextField()
    preview = models.ImageField()
    video_link = models.CharField(max_length=255)

    def __str__(self):
        return self.title
