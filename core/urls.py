from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('verify-email/<int:user_id>/<str:token>/', views.verify_email, name='verify_email'),
    path('login/', views.login, name='login'),
    path('forgot-password/', auth_views.PasswordResetView.as_view(
        template_name='core/forgot_password.html'
    ), name='forgot_password'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='core/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('income/',views.income,name='income'),
    path('expense/',views.expense,name='expense'),
    path('budget/',views.budget,name='budget'),
    path('goal/',views.goal,name='goal'),
    path('delete-goal/<int:id>/', views.delete_goal, name='delete_goal'),
    path('reports/', views.reports, name='reports'),
    path('savings/', views.savings, name='savings'),
    
]