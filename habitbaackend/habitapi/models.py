from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    frequency = models.CharField(max_length=10, choices=[("daily", "Daily"), ("weekly", "Weekly")])
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

class CheckIn(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  # allow null temporarily
    note = models.TextField(blank=True, null=True)

