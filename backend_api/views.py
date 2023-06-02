# from django.shortcuts import render
from rest_framework.views import APIView
# from . import models
from .models import Material
# from .serializer import MaterialSerializers
from rest_framework.response import Response
# Объекты Q обеспечивают полный контроль над пунктом where запроса.
from django.db.models import Q
from django.http import JsonResponse
# from django.http import HttpResponse
# Create your views here.
# РЕГИСТРАЦИЯ
# csrf_exempt
# пользователя выполнить нежелательное действие на доверенном сайте,
# на котором пользователь авторизован.
from django.views.decorators.csrf import csrf_exempt
# User являются ядром системы аутентификации.
# Они обычно представляют людей, взаимодействующих с вашим сайтом,
# и используются для таких вещей,
# как ограничение доступа, регистрация профилей пользователей,
# ассоциирование контента с создателями и т.д.
from django.contrib.auth.models import User
import json
# АУТЕНТИФИКАЦИЯ
# authenticate() проверка учетных данных.
# Она принимает учетные данные в качестве аргументов ключевых слов,
# username и password по умолчанию,
# сверяет их с каждым authentication backend и возвращает объект User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
# Использование класса APIView практически не отличается от использования обычного класса View,
# как обычно, входящий запрос отправляется в соответствующий метод-обработчик,
# такой как .get() или .post().
# Кроме того, для класса может быть установлен ряд атрибутов,
# которые контролируют различные аспекты политики API.
from rest_framework.decorators import api_view


class MaterialView(APIView):
    def get(self, request):
        output = [
            {
                "idProduct": output.idProduct,
                "title": output.title,
                "name": output.name,
                "img": output.img,
                "brand": output.brand,
                "price": output.price,
                "screenSize": output.screenSize,
                "memoryCard": output.memoryCard,
                "cpu": output.cpu,
                "videoCard": output.videoCard,
            }
            for output in Material.objects.all()
        ]
        return Response(output)


def get_filtered_products(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
#  Q используется для создания сложных запросов в базу данных и
# комбинировать несколько условий с помощью логических операторов ИЛИ и И.
    products = Material.objects.filter(
        Q(price__gte=min_price) & Q(price__lte=max_price))

    # возвращаем отфильтрованные товары
    return JsonResponse({'data': list(products.values())})


@csrf_exempt
def user_registration(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data['name']
            email = data['email']
            password = data['password']
            user = User.objects.create_user(
                username=email, email=email, password=password)
            user.first_name = name
            user.save()
            return JsonResponse({'message': 'Пользователь успешно зарегистрирован'}, status=201)
        except:
            return JsonResponse({'error': 'Неверный запрос'}, status=400)
    else:
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)


# @csrf_exempt


# api_view По умолчанию принимаются только методы GET.
# Другие методы будут отвечать "405 Method Not Allowed".
# Чтобы изменить это поведение, укажите, какие методы разрешены представлению,
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(username=email, password=password)
    if user is None:
        return Response({'error': 'Неверный email или пароль'}, status=400)
    refresh = RefreshToken.for_user(user)
    return Response({'access': str(refresh.access_token), 'refresh': str(refresh)}, status=200)


# @api_view(['POST'])
def refresh_token(request):
    refresh_token = request.data.get('refresh_token')
    try:
        token = RefreshToken(refresh_token)
        access_token = str(token.access_token)
        return Response({'access': access_token}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
