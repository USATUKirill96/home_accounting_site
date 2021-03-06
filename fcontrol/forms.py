from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.utils.translation import gettext as _
from django.utils.html import format_html
from datetime import date


class IncomeAddForm(forms.Form):
    date = forms.DateField(widget=forms.widgets.SelectDateWidget(), initial=date.today())
    name = forms.CharField(required=False, label="Источник")
    sum = forms.IntegerField(label="Сумма")


class IncomeEditForm(IncomeAddForm):
    operation_id = forms.IntegerField(widget=forms.widgets.HiddenInput)


MONTHS = ((1, "январь"), (2, "февраль"), (3, "март"), (4, "апрель"), (5, "май"), (6, "июнь"),
          (7, "июль"), (8, "август"), (9, "сентябрь"), (10, "октябрь"), (11, "ноябрь"), (12, "декабрь"))


class IncomesPeriodForm(forms.Form):
    month = forms.ChoiceField(choices=MONTHS, initial=date.today().month.as_integer_ratio())
    year = forms.IntegerField(initial=date.today().year)


CATEGORIES = (("Другое", "другое"), ("Продукты", "продукты"), ("Развлечения", "развлечения"),
              ("Бытовые", "бытовые"), ("Здоровье", "здоровье"), ("Транспорт", "транспорт"),
              ("Животные", "животные"))


class LimitationForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORIES, label="Категория")
    sum = forms.IntegerField(label="Лимит в месяц")


class OldLimitationForm(forms.Form):
    def __init__(self, *args, **kwargs):
       super(OldLimitationForm, self).__init__(*args, **kwargs)
       self.fields['category'].widget.attrs['readonly'] = True

    category = forms.CharField(label="Категория")
    sum = forms.IntegerField(label="Лимит в месяц")
