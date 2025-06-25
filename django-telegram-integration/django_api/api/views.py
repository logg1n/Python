from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
import json
import secrets

User = get_user_model()

@csrf_exempt
@require_GET
def get_user_info(request):
    telegram_id = request.GET.get('telegram_id')
    if not telegram_id:
        return JsonResponse({'error': 'Не указан telegram_id'}, status=400)

    try:
        user = User.objects.get(telegram_id=telegram_id)
        return JsonResponse({
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'Пользователь не найден'}, status=404)

from django.conf import settings

@csrf_exempt
@require_POST
def register_telegram_user(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        telegram_id = data.get('telegram_id')

        if not email or not telegram_id:
            return JsonResponse({'error': 'Нужно указать email и telegram_id'}, status=400)

        existing = User.objects.filter(telegram_id=telegram_id).first()
        if existing:
            return JsonResponse({'error': 'Этот Telegram ID уже привязан к пользователю'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            if settings.ALLOW_TELEGRAM_AUTO_CREATE:
                user = User(email=email, username=email.split('@')[0])
                user.set_password(secrets.token_urlsafe(12))
                user.save()
            else:
                return JsonResponse({'error': 'Пользователь с таким email не найден'}, status=404)

        user.telegram_id = telegram_id
        user.save()

        return JsonResponse({'message': 'Telegram ID успешно привязан'})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Невалидный JSON'}, status=400)

