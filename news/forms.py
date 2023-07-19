from django import forms
from django.core.exceptions import ValidationError
from .models import Post


# Создаем собственный класс формы, наследуемый от ModelForm
class PostForm(forms.ModelForm):

    class Meta:
        # Прописываем саму модель
        model = Post
        # используем все поля, кроме первичного ключа (id), в дальнейшем лучше самостоятельно
        # указывать нужные поля, для невозможности редактирования пользователем неизменяемых полей.
        # fields = '__all__'
        fields = [
            'author',
            'post_category',
            'post_title',
            'post_text',
        ]

    # Переопределим метод clean и реализуем в нем проверку.
    def clean(self):
        cleaned_data = super().clean()
        post_title = cleaned_data.get("post_title")
        if post_title is not None and len(post_title) < 3:
            raise ValidationError({
                "post_title": "Заголовок статьи не может быть менее трех символов или пустым."
            })
        return cleaned_data
