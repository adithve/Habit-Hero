
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
    path('api/habits/analytics/', views.user_habits_with_stats),
    path('api/logout/', views.logout_view),
    path('api/best-date/', views.best_checkin_date),
]
