from django import template

register = template.Library()

# Сообщаем Django, что для работы нужно передать контекст который мы редактировали
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    # Копируем параметры текущего запроса
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()