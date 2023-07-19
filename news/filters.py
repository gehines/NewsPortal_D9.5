from django_filters import FilterSet, DateFilter
from .models import Post, Author


# Создаем свой набор фильтров для модели Post.
# Наследуемый FilterSet, похож на дженереки.
class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],  # Совпадение, частичное, без учета регистра
            'author': ['exact'],  # Точное совпадение по автору
            'date_of_post': ['gt']  # Дата позже
        }
