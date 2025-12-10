from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # предыдущий url входа
    # path('login/', views.user_login, name='login'),
    # url-адреса входа и выхода
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # url-адреса смены пароля
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('register/', views.register, name='register'),

    path('', views.home_page, name='home_page'),

    path('history/', views.history_view, name='history'),

    path('history/delete/<int:calc_id>/', views.delete_calculation, name='delete_calculation'),
    path('history/pdf/<int:calc_id>/', views.pdf_calculation, name='pdf_calculation'),
]