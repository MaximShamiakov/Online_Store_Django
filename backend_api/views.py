from django.shortcuts import render
from rest_framework.views import APIView
from . import models
from .models import Material
from .serializer import MaterialSerializers
from rest_framework.response import Response
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse
# Create your views here.


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
