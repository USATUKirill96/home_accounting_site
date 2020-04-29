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


@login_required
def edit_income(request):
    if request.method == "GET":
        date = request.GET.get('date')
        name = request.GET.get('name')
        sum = request.GET.get('sum')
        operation_id = request.GET.get('operation_id')
        formatted_date = datetime.strptime(date, "%d-%m-%Y").date
        incomes_form = IncomeEditForm(initial={'date': formatted_date, 'name': name,
                                               'sum': sum, 'operation_id': operation_id})
        return render(request, 'fcontrol/edit_income.html', {'section': 'edit_income', 'incomes_form': incomes_form})
    else:
        incomes_form = IncomeEditForm(request.POST)
        if incomes_form.is_valid():
            date = incomes_form.cleaned_data['date']
            name = incomes_form.cleaned_data['name']
            sum = incomes_form.cleaned_data['sum']
            operation_id = incomes_form.cleaned_data['operation_id']
        # if True:
        #     date = incomes_form.data['date'].clean()
        #     name = incomes_form.data['name']
        #     sum = incomes_form.data['sum']
        #     operation_id = incomes_form.data['operation_id']
            requests.put('http://localhost:8000/api/incomes/', data={'user_id': request.user.pk,
                                                                     'source': 'site',
                                                                     'date': date,
                                                                     'name': name, 'sum': sum,
                                                                     'operation_id': operation_id, })
            return redirect('fcontrol:incomes')

        return render(request, 'fcontrol/edit_income.html', {'section': 'dashboard', 'incomes_form': incomes_form})


@login_required
def remove(request, operation_id):
    """Delete the spending and redirect to the main page"""
    requests.delete(f'http://localhost:8000/api/incomes?operation_id={operation_id}&user_id={request.user.pk}&source=site')
    return redirect('fcontrol:incomes')