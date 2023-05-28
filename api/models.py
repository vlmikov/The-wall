from django.db import models

class ConfigWall(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    conf = models.TextField()

    class Meta:
        ordering = ['-created']
