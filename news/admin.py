from django.contrib import admin
from .models import Post, Category

# Register your models here.
# Регестрируем наши (пока две) модели, иначе мы их не увидим

admin.site.register(Category)
admin.site.register(Post)