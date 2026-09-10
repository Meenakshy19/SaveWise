from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
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