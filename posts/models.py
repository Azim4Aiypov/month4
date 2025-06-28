from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=256)
    content = models.TextField(null=True, blank=True)  # Лучше TextField для контента
    rate = models.IntegerField(default=0)  # Числовое поле, default=0
    created_at = models.DateTimeField(auto_now_add=True)  # Обычно без null=True
    updated_at = models.DateTimeField(auto_now=True)  # Обычно без null=True
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
