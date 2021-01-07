# Django
from django.db import models


class TodoItem(models.Model):
    description = models.TextField()

    def get_absolute_url(self):
        return f"/todos/{self.id}/"
