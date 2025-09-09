from django import forms
from django.core.exceptions import ValidationError
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Введите текст цитаты'}),
            'source': forms.TextInput(attrs={'placeholder': 'Автор или источник цитаты'})
        }
        labels = {
            'text': 'Текст цитаты',
            'source': 'Автор/Источник',
            'weight': 'Вес цитаты (чем больше, тем чаще показывается)'
        }
        help_texts = {
            'weight': 'Рекомендуемое значение: 1-100'
        }

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 20:
            raise ValidationError('Текст цитаты должен быть не менее 20 символов')
        return text

    def clean_source(self):
        source = self.cleaned_data['source']
        if len(source) < 3:
            raise ValidationError('Укажите корректного автора или источник цитаты')
        return source

    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if weight < 1 or weight > 100:
            raise ValidationError('Вес должен быть в диапазоне от 1 до 100')
        return weight