from django.db import models


class Index(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content