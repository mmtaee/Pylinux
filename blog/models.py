from django.db import models

class HomeRequest(models.Model):
    num = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.date)


class BlogRequest(models.Model):
    num = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.date)