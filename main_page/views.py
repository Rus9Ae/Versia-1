from django.shortcuts import render, redirect
from .models import *
import telebot
import requests


bot = telebot.TeleBot("5634171580:AAFFT_5XJ7cdI3s3chYZtK99jPD7iAmOBBI")

def index_page(request):
    #Если отправят отзыв
    if request.method == 'POST':
        mail = request.POST.get('mail')
        feedback = request.POST.get("message")

        Feedback.objects.create(user_mail=mail, feedback_message=feedback)

    connect = requests.get(url="https://cbu.uz/ru/arkhiv-kursov-valyut/json/").json()
    weather1 = requests.get('https://api.openweathermap.org/data/2.5/weather?q={Tashkent}&appid='
                            '{f915f3fc8b4d935cbb8faef5855b2cbb}')


    products = Product.objects.all()
    categories = Category.objects.all()
    sales = Sale.objects.all()
    currency_rate = connect[0]['Rate']
    weather = weather1.json()

    return render(request, 'index.html', {"products": products,
                                          "categories": categories,
                                          "sales": sales,
                                          "currency_rate": currency_rate,
                                          "weather": weather})

# Функция поиска
def search_product(request):
    if request.method == "POST":
        user_search_product = request.POST.get("search")
        try:
            result_product = Product.objects.get(product_name=user_search_product)
            return render(request, 'current_product.html',
                          {'result_product' : result_product})

        except:
            return redirect('/')


#Получить опреленый продукт
def current_product(request, name, pk):
    product = Product.objects.get(product_name=name, id=pk)

    return render(request, 'current_product.html',
                  {"result_product" : product})


#Получить категории продуктов
def category_product(request, pk):
    category = Category.objects.get(id=pk)

    product_from_category = Product.objects.filter(product_category=category)

    return render(request, 'category_product.html',
                  {"product_from_category" : product_from_category})


# Добавление в корзину
def add_product_to_user_cart(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        product_count = int(request.POST.get('count'))

        user = Cart(user_id=request.user.id,
                    user_product=product,
                    product_quantity=product_count,
                    total_for_current_product=product_count*product.product_price)

        product.product_quantity -= product_count
        product.save()
        user.save()

        return redirect(f"/product/{product.product_name}/{pk}")


def cart_product(request):
    cart_user = Cart.objects.filter(user_id=request.user.id)
    #Итог
    total = sum([i.total_for_current_product for i in cart_user])

    context = {"cart_user": cart_user, "total": total}

    return render(request, "cart_user.html", context)

# Удаление продукта из корзины
def delete_product_from_cart(request, pk):
    if request.method == "POST":
        delete_product = Cart.objects.get(id=pk, user_id=request.user.id)

        product = Product.objects.get(product_name=delete_product.user_product)
        product.product_quantity += delete_product.product_quantity

        product.save()
        delete_product.delete()

        return redirect('/cart')

def confirm_order(request):
    if request.method == "POST":
        current_user_cart = Cart.objects.filter(user_id=request.user.id)

        #Получаем все значения из front части
        client_name = request.POST.get("client_name")
        client_address = request.POST.get("client_address")
        client_number = request.POST.get("client_number")
        client_comment = request.POST.get("client_comment")

        #Формулировка сообщения для админа в тг
        full_message = f'Новый заказ(с сайта)\n' \
                       f'\nИмя: {client_name}' \
                       f'\nАдрес: {client_address}' \
                       f'\nНомер телефона: {client_number}' \
                       f'\nКомментарий к заказу: {client_comment}'

        for i in current_user_cart:
            full_message += f'Продукт {i.user_product}' \
                            f'\nКоличество: {i.product_quantity}' \
                            f'\nСумма {i.total_for_current_product} сум\n----------\n'

            #Отправка сообщения
        bot.send_message(65723925, full_message)

        return redirect('/')








