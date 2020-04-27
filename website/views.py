import requests
from datetime import date as currentdate
from datetime import datetime
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import *


class PasswordChangeCustom(auth_views.PasswordChangeView):
    form_class = CustomPasswordChange


@login_required
def dashboard(request):
    """main page, observes user's spendings and allows to add/redact/delete it"""
    if request.method == 'POST':
        # requesting the forms data
        spends_form = SpendsAddForm(request.POST)
        period_form = SpendsPeriodForm(request.POST)
        if spends_form.is_valid():
            # user added new information to the database
            date = spends_form.cleaned_data['date']
            category = spends_form.cleaned_data['category']
            name = spends_form.cleaned_data['name']
            sum = spends_form.cleaned_data['sum']
            requests.post('http://localhost:8000/api/spends/', data={'user_id': request.user.pk, 'source': 'site',
                                                                     'category': category, 'date': date,
                                                                     'name': name, 'sum': sum, 'common': 'False'})
            messages.success(request, 'Расход добавлен в таблицу')
        else:
            # user just opened another part of spends (changed month, year)
            spends_form = SpendsAddForm(initial={'date': currentdate.today()})

        if period_form.is_valid():
            # user changed month/year of spends
            month = period_form.cleaned_data['month']
            year = period_form.cleaned_data['year']
        else:
            # user added another spending
            if spends_form.is_valid():
                month = date.month
                year = date.year
            else:
                month = currentdate.today().month
                year = currentdate.today().year

            period_form = SpendsPeriodForm(initial={'year': year, 'month': month})
        spends = requests.get(
            f'http://localhost:8000/api/spends?user_id={request.user.pk}&source=site&month={month}&year={year}')
    else:
        # if the type of request if GET
        # initialize the forms with current data
        spends_form = SpendsAddForm(initial={'date': currentdate.today()})
        period_form = SpendsPeriodForm(
            initial={'year': currentdate.today().year, 'month': currentdate.today().month})
        spends = requests.get(
            f'http://localhost:8000/api/spends?user_id={request.user.pk}&source=site&'
            f'month={currentdate.today().month}&year={currentdate.today().year}')
    spends = spends.json()
    return render(request, 'website/dashboard.html', {'section': 'dashboard', 'spends_form': spends_form,
                                                      'period_form': period_form, 'spends': spends['Spendings']})


@login_required
def remove(request, spending_id):
    """Delete the spending and redirect to the main page"""
    requests.delete(f'http://localhost:8000/api/spends/?spending_id={spending_id}')
    return redirect('/')


@login_required
def edit_spending(request):
    if request.method == "GET":
        date = request.GET.get('date')
        category = request.GET.get('category')
        name = request.GET.get('name')
        sum = request.GET.get('sum')
        spending_id = request.GET.get('spending_id')
        formatted_date = datetime.strptime(date, "%d-%m-%Y").date
        spends_form = SpendsRedactForm(initial={'category': category, 'date': formatted_date, 'name': name,
                                                'sum': sum, 'spending_id': spending_id})
        return render(request, 'website/edit_spending.html', {'section': 'edit_spending', 'spends_form': spends_form})
    else:
        spends_form = SpendsRedactForm(request.POST)
        if spends_form.is_valid():
            category = spends_form.cleaned_data['category']
            date = spends_form.cleaned_data['date']
            name = spends_form.cleaned_data['name']
            sum = spends_form.cleaned_data['sum']
            spending_id = spends_form.cleaned_data['spending_id']
            requests.put('http://localhost:8000/api/spends/', data={'user_id': request.user.pk,
                                                                    'source': 'site',
                                                                    'category': category, 'date': date,
                                                                    'name': name, 'sum': sum,
                                                                    'spending_id': spending_id,})
            return redirect('/')

        return render(request, 'website/edit_spending.html', {'section': 'dashboard', 'spends_form': spends_form,
                                                              'error': True})


def register(request):
    if request.method == 'POST':
        user_form = CustomUserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password1'])
            # Сохраняем пользователя в базе данных.
            new_user.save()
            # Создание профиля пользователя
            requests.post('http://127.0.0.1:8000/api/users/', data={'user_id': str(new_user.pk)})
            return render(request,
                          'website/register_done.html',
                          {'new_user': new_user})

    else:
        user_form = CustomUserRegistrationForm()
    return render(request, 'website/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Профиль успешно обновлен')
        else:
            messages.error(request, 'Ошибка при обновлении профиля')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'website/edit.html',
                  {'user_form': user_form})

@login_required
def main(request):
    return render(request, 'website/main.html')