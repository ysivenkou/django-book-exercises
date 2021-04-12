# from django.forms import ModelForm
from django import forms

from .models import Bb, Rubric
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# class BbForm(ModelForm):
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')


class BbForm(forms.ModelForm):
    title = forms.CharField(label='Название товара')
    content = forms.CharField(label='Описание', widget=forms.widgets.Textarea())
    price = forms.DecimalField(label='Цена', decimal_places=2)

    # published = forms.DateField(
    #     label='Дата публикации',
    #     widget=forms.widgets.SelectDateWidget(
    #         empty_label=('Выберите год', 'Выберите месяц', 'Выберите число')
    #     )
    # )

    rubric = forms.ModelChoiceField(
        queryset = Rubric.objects.all(),
        label='Рубрика',
        help_text='Не забудьте задать рубрику',
        widget=forms.widgets.Select(attrs={'size': Rubric.objects.count() + 1})
    )

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')

    def clean_title(self):
        val = self.cleaned_data['title']
        if val == 'Прошлогодний снег':
            raise ValidationError('К продаже не допускается')
        return val

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data['content']:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if self.cleaned_data['price'] < 0:
            errors['price'] = ValidationError('Укажите неотрицательное значение цены')
        if errors:
            raise ValidationError(errors)


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повторите пароль')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
