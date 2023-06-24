from django.db import models
# временная зона в которой мы находимся
from django.utils import timezone
# стондартные user django
from django.contrib.auth.models import User


class Material(models.Model):
    # Заголовок материала
    idProduct = models.CharField(max_length=250, blank=True)
    title = models.CharField(max_length=250, blank=True)
    name = models.CharField(max_length=250, blank=True)
    img = models.CharField(max_length=250,  blank=True)
    brand = models.CharField(max_length=250, blank=True)
    price = models.IntegerField(blank=True)
    screenSize = models.CharField(max_length=250, blank=True)
    memoryCard = models.CharField(max_length=250, blank=True)
    cpu = models.CharField(max_length=250, blank=True)
    videoCard = models.CharField(max_length=250, blank=True)

    # Слаг - это унекальн индефикатор обьекта
    # slaug = models.SlugField(max_length=255, unique_for_date="publish")
    # даты публикации
    # добовляем timezone.now
    publish = models.DateTimeField(default=timezone.now)
    # пробивает дату запроса
    updated = models.DateTimeField(auto_now=True)
    # пробивает когда обьект добавляется в базу данных
    created = models.DateTimeField(auto_now_add=True)
    # Автор творения
    author = models.ForeignKey(
        # User - указывает таблицу связанную с нашим полем
        User,
        # on_delete=models.CASCADE - при удалении пользывотеля, удаляются все его мотериалы
        on_delete=models.CASCADE,
        # related_name='user_materials' - получение всех материалов у автора к которым он имеет отнашения
        related_name="user_materials",
    )


class NewUser(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=30)


class NewKey(models.Model):
    key = models.CharField(max_length=128, unique=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)


class Basket(models.Model):
    key = models.CharField(max_length=255, default='')
    product_id = models.CharField(max_length=255, default='')
    quantity = models.PositiveBigIntegerField()
