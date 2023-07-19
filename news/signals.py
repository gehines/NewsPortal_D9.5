from django.dispatch import receiver
from django.db.models.signals import m2m_changed # Сигнал будет отправлятся при изменении поля ManyToMany модели
from .models import PostCategory
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_notify(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_send.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    message = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    message.attach_alternative(html_content, 'text/html')
    message.send()

# В декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
@receiver(m2m_changed, sender=PostCategory)
def new_post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [name.email for name in subscribers]

        send_notify(instance.preview(), instance.pk, instance.title, subscribers)
