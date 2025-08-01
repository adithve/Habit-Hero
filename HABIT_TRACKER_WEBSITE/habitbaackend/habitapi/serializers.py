from rest_framework import serializers
from .models import Habit, CheckIn
from datetime import date

class HabitSerializer(serializers.ModelSerializer):
    completed_today = serializers.SerializerMethodField()
    note_today = serializers.SerializerMethodField()  # <-- Add this line

    class Meta:
        model = Habit
        fields = [
            'id', 'name', 'category', 'frequency',
            'start_date', 'created_at', 'active',
            'completed_today', 'note_today'  # <-- Include this
        ]

    def get_completed_today(self, habit):
        user = self.context['request'].user
        today = date.today()
        return CheckIn.objects.filter(habit=habit, user=user, date=today).exists()

    def get_note_today(self, habit):
        user = self.context['request'].user
        today = date.today()
        checkin = CheckIn.objects.filter(habit=habit, user=user, date=today).first()
        return checkin.note if checkin and checkin.note else None
