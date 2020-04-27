import requests
from datetime import date as currentdate
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *


def main(request):
    return render(request, 'fcontrol/main.html')


@login_required
def incomes(request):
    """main page, observes user's incomes and allows to add/redact/delete it"""
    if request.method == 'POST':
        # requesting the forms data
        incomes_form = IncomeAddForm(request.POST)
        period_form = IncomesPeriodForm(request.POST)
        if incomes_form.is_valid():
            # user added new information to the database
            date = incomes_form.cleaned_data['date']
            name = incomes_form.cleaned_data['name']
            sum = incomes_form.cleaned_data['sum']
            requests.post('http://localhost:8000/api/incomes/', data={'user_id': request.user.pk, 'source': 'site',
                                                                     'date': date,
                                                                     'name': name, 'sum': sum})
            messages.success(request, 'Успешно добавлено')
        else:
            # user just opened another part of spends (changed month, year)
            incomes_form = IncomeAddForm(initial={'date': currentdate.today()})

        if period_form.is_valid():
            # user changed month/year of spends
            month = period_form.cleaned_data['month']
            year = period_form.cleaned_data['year']
        else:
            # user added another spending
            if incomes_form.is_valid():
                month = date.month
                year = date.year
            else:
                month = currentdate.today().month
                year = currentdate.today().year

            period_form = IncomesPeriodForm(initial={'year': year, 'month': month})
        incomes = requests.get(
            f'http://localhost:8000/api/incomes?user_id={request.user.pk}&source=site&month={month}&year={year}')
    else:
        # if the type of request if GET
        # initialize the forms with current data
        incomes_form = IncomeAddForm(initial={'date': currentdate.today()})
        period_form = IncomesPeriodForm(
            initial={'year': currentdate.today().year, 'month': currentdate.today().month})
        incomes = requests.get(
            f'http://localhost:8000/api/incomes?user_id={request.user.pk}&source=site&'
            f'month={currentdate.today().month}&year={currentdate.today().year}')
    incomes = incomes.json()
    return render(request, 'fcontrol/incomes.html', {'section': 'incomes', 'incomes_form': incomes_form,
                                                      'period_form': period_form, 'incomes': incomes["Incomes"]})

