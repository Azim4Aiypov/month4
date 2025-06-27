from django.contrib import admin
from .models import Post, Category, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "rate", "created_at", "updated_at", "category"]
    list_editable = ["rate"]
    list_filter = ["created_at", "updated_at", "category", "tags"]
    list_per_page = 2

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
