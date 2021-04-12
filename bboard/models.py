from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
# from django.core.exceptions import NON_FIELD_ERRORS


class Bb(models.Model):
    title = models.CharField(
        max_length=50,
        validators=[validators.RegexValidator(regex='^.{4,}$')],
        error_messages={'blank': 'Название объявления отсутствует. Пожалуйста, введите название объявления'},
        verbose_name='Товар',
    )
    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )
    price = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Цена',
    )
    published = models.DateTimeField(
        auto_now_add=True, 
        db_index=True,
        verbose_name='Опубликовано',
    )
    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        # запрет на удаление: рубрика не сможет удалиться, если в модели объявлений есть хотя бы одно объявление с данной тематикой
        # Таким образом, модель рубрик является первичной, а модель объявлений - вторичной
        on_delete=models.PROTECT, 
        # просто имя, по которому можно обратиться к вторичной модели. Никакой связи с полями вторичной модели!
        related_name='entries',
        related_query_name='entry',
        verbose_name='Рубрика',
    )

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['rubric', 'title']
        unique_together = [
            ('title', 'published'),
            ('title', 'price', 'rubric'),
        ]
        get_latest_by = 'published'
        # order_with_respect_to = 'rubric'
        indexes = [
            models.Index(fields=['-published', 'title'], name='bb_main'),
            models.Index(fields=['title', 'price', 'rubric'], name='bb_alter', condition=models.Q(price__lte=10000)),
        ]

    def title_and_price(self):
        if self.price:
            return '%s {%.2f}' % (self.title, self.price)
        else:
            return self.title
    title_and_price.short_description = 'Название и цена'

    def clean(self):
        self.errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите неотрицательное значение цены')
        if self.errors:
            raise ValidationError(errors)


class Rubric(models.Model):
    name = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name='Название',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Названия'
        verbose_name = 'Название'
        ordering = ['name']

class AdvUser(models.Model):
    is_activated = models.BooleanField(
        default=True,
        verbose_name='Активирован',
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
