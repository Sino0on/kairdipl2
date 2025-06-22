from idlelib.rpc import request_queue
from random import shuffle

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
from pprint import pprint
from decouple import config

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Product, Category
from random import sample


def products_list(request):
    category_id = request.GET.get('id_group')

    # Фильтрация по категории
    if category_id:
        products = Product.objects.filter(category__id=category_id)
        categories = Category.objects.filter(id=category_id)
    else:
        products = Product.objects.all()
        categories = Category.objects.all()  # Или фильтр под главные категории

    # Пагинация
    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    # Кастомный range для пагинации
    current_page = paginated_products.number
    total_pages = paginator.num_pages
    max_visible = 4
    half = max_visible // 2

    if total_pages <= max_visible:
        custom_page_range = range(1, total_pages + 1)
    else:
        start = max(current_page - half, 1)
        end = min(start + max_visible - 1, total_pages)
        start = max(end - max_visible + 1, 1)
        custom_page_range = range(start, end + 1)

    context = {
        "products": paginated_products.object_list,
        "paginator": paginator,
        "page_obj": paginated_products,
        "is_paginated": paginated_products.has_other_pages(),
        "custom_page_range": custom_page_range,
        "categories": categories,
    }

    if category_id:
        context['params'] = category_id

    return render(request, 'index.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    # Случайные продукты для "похожие товары"
    other_products = list(Product.objects.exclude(id=pk))
    suggested_products = sample(other_products, min(4, len(other_products)))

    return render(request, 'productDetail.html', {
        'product': product,
        'products': suggested_products
    })

# def update_data(request, test=None):

    #
    # # URL для запроса
    # url = "https://app.pos-service.kg/proxy/?path=%2Fdata%2F64abd976dac244c8d30a926c%2Fcatalog%2F%3Flimit%3D1000%26offset%3D0&api=v3&timezone=21600"
    #
    # # Заголовок с cookies
    # cookies = {
    #     "connect.sid": config("CONNECT_ID"),
    #     "company_id": config("COMPANY_ID"),
    # }
    #
    # response = requests.get(url, cookies=cookies)
    #
    # if response.status_code == 200:
    #     # print("Ответ получен успешно!")
    #     data = response.json()
    #     dastan = []
    #     categories = []
    #     # print(len(data['data']))
    #     for i in range(len(data['data'])):
    #         if data["data"][i]['type'] != 'group':
    #
    #             a =  {
    #                 (k[1:] if k.startswith('_') else k): v
    #                 for k, v in data["data"][i].items()
    #             }
    #             dastan.append(a)
    #         else:
    #             a = {
    #                 (k[1:] if k.startswith('_') else k): v
    #                 for k, v in data["data"][i].items()
    #             }
    #             categories.append(a)
    #     with open('db.json', 'w', encoding='utf-8') as f:
    #         json.dump(dastan[::-1], f, ensure_ascii=False, indent=4)
    #     with open('categories.json', 'w', encoding='utf-8') as f:
    #         json.dump(categories[::-1], f, ensure_ascii=False, indent=4)
    #     if not test:
    #         return HttpResponse("ok")
    # else:
    #     if not test:
    #         return HttpResponse("error")
