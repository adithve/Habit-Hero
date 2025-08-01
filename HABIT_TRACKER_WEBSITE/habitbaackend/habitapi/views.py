import json
from datetime import date
from datetime import datetime 
from rest_framework import status
from .models import Habit, CheckIn
from datetime import timedelta, date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from habitapi.serializers import HabitSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated






from collections import defaultdict
from .models import Habit, CheckIn
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from .models import Habit, CheckIn
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token



#signup
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



#login
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

#add
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

#dashboard
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_habits(request):
    habits = Habit.objects.filter(user=request.user)
    serializer = HabitSerializer(habits, many=True, context={'request': request})
    return Response(serializer.data)


#edit
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
    
#delete
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
    
#togglebutton
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

    # chcking habit's start date
    if habit.start_date > today:
        return Response(
            {'error': 'Habit tracking cannot start before the start date.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        checkin = CheckIn.objects.get(habit=habit, user=user, date=today)
        checkin.delete()
        return Response({'status': 'unchecked'}, status=status.HTTP_200_OK)

    except CheckIn.DoesNotExist:
        checkin = CheckIn.objects.create(habit=habit, user=user, date=today)
        return Response({
            'status': 'checked',
            'id': checkin.id,
            'habit': habit.id,
            'user': user.id,
            'date': checkin.date
        }, status=status.HTTP_200_OK)

#analytics
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_view(request):
    user = request.user
    habits = Habit.objects.filter(user=user)
    today = date.today()
    result = []

    for habit in habits:
        checkins = CheckIn.objects.filter(habit=habit, user=user).order_by('date')
        checkin_dates = [check.date for check in checkins]

        # Calculate current streak
        current_streak = 0
        for i in range(len(checkin_dates)-1, -1, -1):
            if (today - checkin_dates[i]).days == current_streak:
                current_streak += 1
            else:
                break

        # Calculate longest streak
        longest_streak = 0
        streak = 1
        for i in range(1, len(checkin_dates)):
            if (checkin_dates[i] - checkin_dates[i-1]).days == 1:
                streak += 1
            else:
                longest_streak = max(longest_streak, streak)
                streak = 1
        longest_streak = max(longest_streak, streak)

        # Success rate
        total_days = (today - habit.start_date).days + 1
        success_rate = round((len(checkin_dates) / total_days) * 100, 2) if total_days > 0 else 0

        # Best days
        day_counts = defaultdict(int)
        for check_date in checkin_dates:
            weekday = check_date.strftime("%A")
            day_counts[weekday] += 1
        sorted_days = sorted(day_counts.items(), key=lambda x: x[1], reverse=True)
        best_days = [day for day, _ in sorted_days[:3]]  # Top 3 best days

        result.append({
            "name": habit.name,
            "category": habit.category,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "success_rate": success_rate,
            "best_days": best_days
        })

    return Response(result)



#addnote
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

#logout
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
