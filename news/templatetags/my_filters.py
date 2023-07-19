from django import template

register = template.Library()

# Создаем словарь со списком плохих слов и символов их заменяющих
BAD_WORDS = {
    'Фигня': 'Ф****',
    'фигня': 'ф****',
    'Попа': 'П***',
    'попа': 'п***',
    'Редиска': 'Р******',
    'редиска': 'р******',
    'Ерунда': 'Е*****',
    'ерунда': 'е*****',
    }

# Регистрируем фильтр под именем censore
# Декоратор указывает Django, что нужно запомнить про существование нового фильтра
# Название фильтра по умолчанию равно названию функции, в шаблонах мы сможем применять {{ post_text|censore }}
# Также мы можем самостоятельно называть фильтр @register.filter(name='censore_mat'),
# не переназывая функцию, тогда в шаблонах фильтр вызывается по его названию.


@register.filter()
def censore(value: str):
    words = value.split(' ')
    new_text = ''

    for i in range(len(words)):
        if words[i] in BAD_WORDS:
            words[i] = BAD_WORDS[words[i]]
            new_text += words[i]
            new_text += ' '
        else:
            new_text += words[i]
            new_text += ' '

    return new_text
