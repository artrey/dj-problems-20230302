from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=40)
    # posts

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    # id
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts',
                                  blank=True)


def reaction(*args, **kwargs):
    print('post was saved')


