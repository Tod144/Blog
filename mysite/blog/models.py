from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", 'Published'
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    author = models.ForeignKey(User, 
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    def ___str__(self):
        return self.title
    
    class Meta:
        ordering = ['-publish'] #сортировка по времени публикации поста, убывающий
        indexes = [
            models.Index(fields=['-publish'])
        ]
