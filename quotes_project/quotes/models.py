from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Quote(models.Model):
    text = models.TextField(
        verbose_name=_('Текст цитаты'),
        help_text=_('Введите полный текст цитаты')
    )
    
    source = models.CharField(
        max_length=255,
        verbose_name=_('Автор/Источник'),
        help_text=_('Укажите автора или источник цитаты')
    )
    
    weight = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        verbose_name=_('Вес цитаты'),
        help_text=_('Определяет частоту показа цитаты (1-100)')
    )
    
    views = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Просмотры')
    )
    
    likes = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Лайки')
    )
    
    dislikes = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Дизлайки')
    )

    class Meta:
        verbose_name = _('Цитата')
        verbose_name_plural = _('Цитаты')
        ordering = ['-views']  # Сортировка по умолчанию по просмотрам

    def __str__(self):
        return f'"{self.text[:30]}..." от {self.source}'

    def increment_views(self):
        self.views += 1
        self.save()

    def add_like(self):
        self.likes += 1
        self.save()

    def add_dislike(self):
        self.dislikes += 1
        self.save()

    def get_rating(self):
        """Возвращает простой рейтинг цитаты"""
        if self.likes + self.dislikes == 0:
            return 0
        return (self.likes - self.dislikes) / (self.likes + self.dislikes)