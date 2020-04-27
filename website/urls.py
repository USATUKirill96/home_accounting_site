from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # login
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # spendings page
    path('spendings/', views.dashboard, name='dashboard'),
    # main page
    path('',views.main, name='main'),
    # password actions
    path('password_change/',
         views.PasswordChangeCustom.as_view(),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    # registration
    path('register/', views.register, name='register'),
    # edit profile
    path('edit/', views.edit, name='edit'),
    path('remove/<int:spending_id>/', views.remove, name='remove'),
    path('edit_spending/', views.edit_spending, name='edit_spendings'),
]
