from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'fcontrol'
urlpatterns = [
    path('', views.main, name='main'),
    path('incomes/', views.incomes, name='incomes'),
    path('edit/', views.edit_income, name='edit'),
    path('remove/<int:operation_id>/', views.remove, name='remove'),
]