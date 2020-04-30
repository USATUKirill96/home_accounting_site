from datetime import date as currentdate
from datetime import datetime

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms import formset_factory

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
    requests.delete(
        f'http://localhost:8000/api/incomes?operation_id={operation_id}&user_id={request.user.pk}&source=site')
    return redirect('fcontrol:incomes')


@login_required
def limitations(request):
    def create_limitation_forms(old_limits):
        """uses formset factory to create personal form for each limitation. Takes json from REST, returns formset"""
        initial_data = []
        for position in old_limits:
            initial_data.append({'category': position['category'], 'sum': position['sum']})
        limitations_factory = formset_factory(OldLimitationForm, extra=0)
        formset = limitations_factory(initial=initial_data)
        return formset

    if request.method == "POST" and "create" in request.POST:
        new_limitation = LimitationForm(request.POST)

        if new_limitation.is_valid():
            category = new_limitation.cleaned_data['category']
            sum = new_limitation.cleaned_data['sum']
            requests.post(f"http://localhost:8000/api/limitations/", data={'user_id': request.user.pk,
                                                                           'source': 'site',
                                                                           'category': category,
                                                                           'sum': sum})
    if request.method == "POST" and "edit" in request.POST:
        limitations_factory = formset_factory(LimitationForm, extra=0)
        limitations_set = limitations_factory(request.POST)

        if limitations_set.is_valid():
            print("da validno")
            for limitation_form in limitations_set.forms:
                if True:
                    sum = limitation_form.cleaned_data['sum']
                    category = limitation_form.cleaned_data['category']
                    requests.put(f"http://localhost:8000/api/limitations/", data={'user_id': request.user.pk,
                                                                                  'source': 'site',
                                                                                  'category': category,
                                                                                  'sum': sum})

    new_limitation = LimitationForm()
    saved_limitations = requests.get(
        f"http://localhost:8000/api/limitations?user_id={request.user.pk}&source=site")
    saved_limitations_json = saved_limitations.json()["Limitations"]
    saved_limitations_forms = create_limitation_forms(saved_limitations_json)
    render_data = {'section': 'limitations', 'limitations': saved_limitations_forms, 'new_limitation': new_limitation}
    return render(request, 'fcontrol/limitations.html', render_data)


@login_required
def delete_limitation(request, category):
    requests.delete(
        f'http://localhost:8000/api/limitations?category={category}&user_id={request.user.pk}&source=site')
    return redirect('fcontrol:limitations')
