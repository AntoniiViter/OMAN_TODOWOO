from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    image = models.ImageField(upload_to='todo/images/', blank=True)
    url = models.URLField(blank=True)
    todocreator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s (%s) [%s]" % (self.title, self.pk, self.todocreator)