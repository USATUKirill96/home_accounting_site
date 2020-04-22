from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.utils.translation import gettext as _
from django.utils.html import format_html
from django.contrib.auth.models import User
from datetime import date

PASSWORD_HELP_TEXT = format_html("""<dl>Ваш пароль не может быть похож на имя пользователя <br>
          Ваш пароль должен содержать как минимум 8 символов <br>
          Пароль не должен быть предсказуем <br>
          Пароль не может состоять из одних цифр</dl>""")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomPasswordChange(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=PASSWORD_HELP_TEXT)


class CustomUserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=PASSWORD_HELP_TEXT)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        labels = {'username': 'Логин'}


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


CHOICES = (("Другое", "другое"), ("Продукты", "продукты"), ("Развлечения", "развлечения"),
               ("Бытовые", "бытовые"), ("Здоровье", "здоровье"), ("Транспорт", "транспорт"),
               ("Животные", "животные"))

class SpendsAddForm(forms.Form):

    date = forms.DateField(widget=forms.widgets.SelectDateWidget(), initial=date.today())
    category = forms.ChoiceField(choices=CHOICES)
    name = forms.CharField(label="Название покупки")
    sum = forms.IntegerField(label="Сумма")
