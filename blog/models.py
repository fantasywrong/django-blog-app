from django.db import models

# Create your models here.
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.user')
    title = models.CharField(max_length=200)
    text = models.TextField()
    # migration test field
    # test = models.TextField()
    create_date = models.DateTimeField(default=timezone.now) # default 값이 now
    publish_date = models.DateTimeField(blank=True, null=True) # 빈 값, null 허용

    def __str__(self):
        return self.title

    def publish(self):
        self.publish_date = timezone.now()
        self.save()