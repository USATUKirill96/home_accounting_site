import requests
import secrets
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

from .forms import CustomUserRegistrationForm, CustomPasswordChange, UserEditForm


class PasswordChangeCustom(auth_views.PasswordChangeView):
    form_class = CustomPasswordChange


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


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
            token = secrets.token_hex(32)
            requests.post('http://127.0.0.1:8000/api/users/', data={'user_id': str(new_user.pk), 'token': token})
    else:
        user_form = CustomUserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


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
    return render(request, 'account/edit.html',
                  {'user_form': user_form})
