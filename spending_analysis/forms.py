from datetime import date
from django import forms

MONTHS = ((None, "Все"), (1, "январь"), (2, "февраль"), (3, "март"), (4, "апрель"), (5, "май"), (6, "июнь"),
          (7, "июль"), (8, "август"), (9, "сентябрь"), (10, "октябрь"), (11, "ноябрь"), (12, "декабрь"))


class PeriodForm(forms.Form):
    month = forms.ChoiceField(choices=MONTHS, required=False, initial=date.today().month.as_integer_ratio())
    year = forms.IntegerField(initial=date.today().year)
