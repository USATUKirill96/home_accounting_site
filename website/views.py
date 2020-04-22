import requests
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

from .forms import CustomUserRegistrationForm, CustomPasswordChange, UserEditForm, SpendsAddForm


class PasswordChangeCustom(auth_views.PasswordChangeView):
    form_class = CustomPasswordChange


@login_required
def dashboard(request):
    if request.method == 'POST':
        spends_form = SpendsAddForm(request.POST)
        if spends_form.is_valid():
            date = spends_form.cleaned_data['date']
            category = spends_form.cleaned_data['category']
            name = spends_form.cleaned_data['name']
            sum = spends_form.cleaned_data['sum']
            requests.post('http://localhost:8000/api/spends/', data={'user_id': request.user.pk, 'source': 'site',
                                                                'category': category,'date': date,
                                                                'name': name, 'sum': sum, 'common': 'False'})
    spends_form = SpendsAddForm()
    spends = requests.get(f'http://localhost:8000/api/spends?user_id={request.user.pk}&source=site')
    spends = spends.json()
    return render(request, 'website/dashboard.html', {'section': 'dashboard', 'spends': spends['Spendings'],
                                                      'spends_form': spends_form})


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
