from django.urls import path
# Импортируем наши представления
from .views import PostsList, PostDetail, PostSearch
from .views import NewsDelete, NewsEdit, NewsCreate
from .views import ArticleEdit, ArticleDelete, ArticleCreate
from .views import IndexView, subscribe, CategoryList


urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),  # при помощи метода as_view представляем наш класс в виде функции
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),  # pk - первичный ключ, выводящийся в шаблоне
                                                                   # (pk можем переназначить в нашем представлении,
                                                                   # наследуемом от класса DetailView: pk_url_kwargs = '***',
                                                                   # в этой переменной по умолчанию стоит 'pk';
                                                                   # int - указывает на целочисленные значения
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', ArticleEdit.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('categories/<int:pk>', CategoryList.as_view(), name='category_news'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('', IndexView.as_view())

]
