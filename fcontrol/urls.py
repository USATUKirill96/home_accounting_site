from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'fcontrol'
urlpatterns = [
    path('', views.main, name='main'),
    path('incomes/', views.incomes, name='incomes'),
    path('edit', views.main, name='edit'),
    path('delete', views.main, name='delete'),
]