from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url
from backend_api.views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", MaterialView.as_view(), name="all material"),
    path('products', get_filtered_products, name='get_filtered_products'),
]
