from datetime import datetime 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User 
import json
from django.contrib.auth import authenticate
from habitapi.serializers import HabitSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated
from datetime import date
from rest_framework import status
from .models import Habit, CheckIn
from datetime import timedelta, date
from collections import defaultdict
from collections import Counter
from datetime import date, timedelta 

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Username and password are required.'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists.'}, status=400)

            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({'message': 'User created successfully.'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method allowed.'}, status=405)




@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_habit_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            name = data.get('name')
            category = data.get('category')
            frequency = data.get('frequency')
            start_date = data.get('start_date')  # Expecting 'YYYY-MM-DD'

            if not all([name, category, frequency, start_date]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            habit = Habit.objects.create(
                user=request.user,
                name=name,
                category=category,
                frequency=frequency,
                start_date=datetime.strptime(start_date, '%Y-%m-%d').date()
            )

            return JsonResponse({'message': 'Habit added successfully.', 'habit_id': habit.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method allowed.'}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_habits(request):
    habits = Habit.objects.filter(user=request.user)
    serializer = HabitSerializer(habits, many=True, context={'request': request})
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_habit_api(request, habit_id):
    try:
        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
        except Habit.DoesNotExist:
            return Response({'error': 'Habit not found'}, status=HTTP_404_NOT_FOUND)

        data = json.loads(request.body)

        # Update fields if provided
        habit.name = data.get('name', habit.name)
        habit.category = data.get('category', habit.category)
        habit.frequency = data.get('frequency', habit.frequency)

        if 'start_date' in data:
            habit.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()

        habit.save()

        return Response({'message': 'Habit updated successfully'}, status=HTTP_200_OK)

    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON'}, status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_habit_api(request, habit_id):
    try:
        habit = Habit.objects.get(id=habit_id, user=request.user)
        habit.delete()
        return Response({'message': 'Habit deleted successfully.'}, status=HTTP_200_OK)
    except Habit.DoesNotExist:
        return Response({'error': 'Habit not found.'}, status=HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
    



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ontoggle(request):
    user = request.user
    habit_id = request.data.get("habit_id")

    try:
        habit = Habit.objects.get(id=habit_id, user=user)
    except Habit.DoesNotExist:
        return Response({'error': 'Habit not found'}, status=status.HTTP_404_NOT_FOUND)

    today = date.today()

    # ❗ Check if habit's start date is in the future
    if habit.start_date > today:
        return Response(
            {'error': 'Habit tracking cannot start before the start date.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        checkin = CheckIn.objects.get(habit=habit, user=user, date=today)
        # Toggle off: Check-in exists, delete it
        checkin.delete()
        return Response({'status': 'unchecked'}, status=status.HTTP_200_OK)

    except CheckIn.DoesNotExist:
        # Toggle on: Check-in doesn't exist, create it
        checkin = CheckIn.objects.create(habit=habit, user=user, date=today)
        return Response({
            'status': 'checked',
            'id': checkin.id,
            'habit': habit.id,
            'user': user.id,
            'date': checkin.date
        }, status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_or_update_note(request, habit_id):
    try:
        habit = Habit.objects.get(id=habit_id, user=request.user)
    except Habit.DoesNotExist:
        return Response({'error': 'Habit not found'}, status=status.HTTP_404_NOT_FOUND)

    today = date.today()

    # ✅ Condition: Prevent adding note before start date
    if habit.start_date > today:
        return Response(
            {'error': 'Habit tracking cannot start before the start date.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    note = request.data.get('note', '').strip()
    if not note:
        return Response({'error': 'Note cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

    checkin, created = CheckIn.objects.get_or_create(
        habit=habit,
        date=today,
        defaults={'user': request.user}
    )

    checkin.note = note
    checkin.save()

    return Response({
        'message': 'Note saved and habit marked as completed for today.',
        'habit_id': habit.id,
        'date': str(today),
        'note': checkin.note,
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        print("User:", request.user)
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        print("Logout error:", e)
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def calculate_daily_streak(checkin_dates):
    if not checkin_dates:
        return 0

    streak = 0
    today = date.today()
    current_day = today

    checkin_set = set(checkin_dates)

    while current_day in checkin_set:
        streak += 1
        current_day = current_day - timedelta(days=1)

    return streak


def calculate_weekly_streak(checkin_dates):
    if not checkin_dates:
        return 0

    streak = 0
    today = date.today()
    current_week_start = today - timedelta(days=today.weekday())

    checkin_weeks = set(
        (d - timedelta(days=d.weekday())).isoformat() for d in checkin_dates
    )

    while current_week_start.isoformat() in checkin_weeks:
        streak += 1
        current_week_start = current_week_start - timedelta(weeks=1)

    return streak

from collections import defaultdict

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_habits_with_stats(request):
    user = request.user
    habits = Habit.objects.filter(user=user)
    result = []

    for habit in habits:
        checkins = CheckIn.objects.filter(user=user, habit=habit).values_list('date', flat=True)
        checkin_dates = sorted(list(set(checkins)))

        # Calculate streak
        if habit.frequency == "daily":
            streak = calculate_daily_streak(checkin_dates)
        else:
            streak = calculate_weekly_streak(checkin_dates)

        # Calculate success rate
        today = date.today()
        start = habit.start_date

        if habit.frequency == "daily":
            total_days = (today - start).days + 1
            completed_days = len([d for d in checkin_dates if start <= d <= today])
            success_rate = (completed_days / total_days * 100) if total_days > 0 else 0

        else:  # weekly
            # Get all week start dates from start to today
            start_week = (start - timedelta(days=start.weekday()))
            current_week = (today - timedelta(days=today.weekday()))
            total_weeks = ((current_week - start_week).days // 7) + 1

            # Group check-ins by week
            checkin_weeks = set(
                (d - timedelta(days=d.weekday())).isoformat() for d in checkin_dates if start <= d <= today
            )
            completed_weeks = len(checkin_weeks)

            success_rate = (completed_weeks / total_weeks * 100) if total_weeks > 0 else 0

        result.append({
            'name': habit.name,
            'category': habit.category,
            'current_streak': streak,
            'success_rate': f"{round(success_rate)}%"
        })

        print(f"{habit.name} | Completed: {completed_days if habit.frequency == 'daily' else completed_weeks} | Expected: {total_days if habit.frequency == 'daily' else total_weeks} | Success Rate: {round(success_rate)}%")

    return Response(result)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def best_checkin_date(request):
    checkins = CheckIn.objects.filter(habit__user=request.user)
    date_counts = Counter(checkin.date for checkin in checkins)

    if not date_counts:
        return Response({'best_date': None, 'count': 0})

    best_date, count = date_counts.most_common(1)[0]
    return Response({'best_date': best_date.strftime("%Y-%m-%d"), 'count': count})