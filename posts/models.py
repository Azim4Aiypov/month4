from django.db import models




class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

# django orm
class Post(models.Model):
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=512, null=True, blank=True)
    rate = models.CharField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title