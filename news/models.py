from django.db import models
# Импортируем реализованную встроенную модель
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


# Создаем модели:
# Автор (содержит объекты всех авторов, а также их рейтинг);
# Категории (темы статей/новостей);
# Статьи (содержит сами новости/статьи которые создают пользователи, с возможностью поставить оценку);
# Промежуточная модель (для связи "многие ко многим");
# Комментарии к статьям (с возможностью поставить оценку);
# on_delete - показывает, что будет происходить с моделью при удалении элемента
# (CASCADE - элемент удаляется со всеми связями).


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    # Метод для подсчета рейтинга автора
    def update_rating(self):
        # Считаем рейтинг статьи автора
        author_posts_rating = Post.objects.all().filter(author_id=self.pk).aggregate(
            posts_rating_sum=Sum('post_rating') * 3
        )

        # Считаем рейтинг комментариев автора
        author_comments_rating = Comment.objects.all().filter(user_id=self.user).aggregate(
            comments_rating_sum=Sum('comment_rating')
        )

        print(author_posts_rating)
        print(author_comments_rating)

        # Обновляем рейтинг автора
        self.author_rating = author_posts_rating['posts_rating_sum'] + author_comments_rating['comments_rating_sum']
        # Сохраняем в БД
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    # Уникальное название категории (не пустое, автоматическое условие в описании модели)
    name_category = models.CharField(max_length=128, unique=True)
    # Добавляем поле для записи пользователей, которые подписаны на обновления в категории
    subscribers = models.ManyToManyField(User, related_name='categories')

    # Добавляем магический метод
    def __str__(self):
        return self.name_category


class Post(models.Model):
    # Создаем список кортежей с указанием возможных типов статей

    NEWS = 'NE'
    ARTICLE = 'AR'

    TYPES = [(NEWS, 'Новость'), (ARTICLE, 'Статья')]

    # ID автора статьи
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Дата и время создания статьи (устанавливается автоматически)
    date_of_post = models.DateTimeField(auto_now_add=True)
    # Категория статьи (связь "многие ко многим"), для реализации связи используется отдельная таблица
    post_category = models.ManyToManyField(Category)
    # Тип статьи с выбором из нашего списка с макимальным значением - 2 символа (будет занимать меньше места в БД)
    type_post = models.CharField(max_length=2, choices=TYPES, default=NEWS)
    # Заголовок статьи
    post_title = models.CharField(max_length=128)
    # Текст статьи
    post_text = models.TextField()
    # Рейтинг статьи
    post_rating = models.IntegerField(default=0)

    # Метод для предварительного просмотра, возвращает первые 124 символа статьи и многоточие в конце
    def preview(self):
        return self.post_text[:125] + '...'

    # Методы для подсчета рейтинга статьи (основан на проставлении оценок Like и DisLike)
    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    # Добавляем магический метод, который возвращает название новости и первые 20 символов
    def __str__(self):
        return f'{self.post_title} : {self.post_text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post_PostCategory = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_PostCategory = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    # ID статьи
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # ID пользователя, оставившего комментарий
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Текст комментария
    text_comment = models.CharField(max_length=255)
    # Время создания комментария
    date_of_comment = models.DateTimeField(auto_now_add=True)
    # Рейтинг комментария
    comment_rating = models.IntegerField(default=0)

    # Методы для подсчета рейтинга комментария
    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
