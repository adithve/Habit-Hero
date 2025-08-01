"""
URL configuration for habitbaackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from habitapi import views

urlpatterns = [
    path('api/signup/', views.signup_api),
    path('api/login/', views.login),
    path('api/add_habit/', views.add_habit_api),
    path('api/ontoggle/', views.ontoggle),
    path('api/habits/', views.list_user_habits),
    path('api/habits/<int:habit_id>/', views.edit_habit_api),
    path('api/delete_habit/<int:habit_id>/', views.delete_habit_api),

    path('api/habit/<int:habit_id>/add-note/', views.add_or_update_note),
    path('api/habits/analytics/', views.analytics_view),
    path('api/logout/', views.logout_view),

]
