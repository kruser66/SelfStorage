import os
import qrcode
from random import choice

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, F, Min, Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.timezone import now, timedelta

from storage.models import Storage
from storage.payments import create_payment, get_payment_status

from .models import Box, Order, Rental, User

from storage.sendmail import send_email, send_email_with_attach, send_email_payment_success


def user_login(request):
    if request.method == "POST":
        email=request.POST['EMAIL']
        password=request.POST['PASSWORD']
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)    
            return redirect('/my-rent')
        
        return redirect("/")


def user_register(request):
    if request.method == "POST":

        email=request.POST['EMAIL_CREATE']
        password=request.POST['PASSWORD_CREATE']
        password_confirm=request.POST['PASSWORD_CONFIRM']
        
        if password == password_confirm:
            user = User.objects.create_user(
                email=email,
                password=password,
                is_staff=False
            )
            user.save()
            login(request, user)
            return redirect("/my-rent")
    return redirect("/")


def recovery_password(request):
    if request.method == "POST":
        email=request.POST['EMAIL_FORGET']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect("/")
        subject = 'SelfStorage: Восстановление пароля'
        message = f'{user.first_name}, Вы запросили восстановление пароля. К сожалению мы не можем его восстановить ))'
        send_email(subject, message, [email])
    return redirect("/")
         

def user_logout(request):
    logout(request)
    return redirect("/")


def edit(request):
    if request.method == "POST":
        user = request.user
        user.email=request.POST['EMAIL_EDIT']
        user.first_name=request.POST['FIRSTNAME_EDIT']
        user.last_name=request.POST['LASTNAME_EDIT']
        user.phonenumber=request.POST['PHONE_EDIT']
        user.save()
    return redirect("/my-rent")    


def index(request):
    storages = Storage.objects.all().prefetch_related('boxes') \
        .annotate(box_min_price=Min(F('boxes__price'))) \
        .annotate(box_count=Count('boxes')) \
        .annotate(box_free=Count('boxes', filter=Q(boxes__busy=False)))
        
    random_storage = choice(storages)
        
    return render(request, 'index.html', {"random_storage": random_storage})


def open_box(request, id):
    rental = Rental.objects.get(id=id)
    client = rental.client.first_name
    storage = rental.box.storage
    box = rental.box.id
    qr_image = qrcode.make(f'{client}, {storage}, {box}, {rental.expired_at}')
    filename = f'{client}-{storage}-Бокс:{box}-{rental.expired_at}.jpg'
    qr_image.save(filename)
    
    subject = 'SelfStorage: QR-код'
    message = f'{client}! \n Высылаем Вам QR-код для открытия Вашей ячейки'
    emails = [rental.client.email]
    send_email_with_attach(subject, message, emails, filename)
    os.remove(filename)

    return redirect("/my-rent")  


def faq(request):
    return render(request, 'faq.html')


def my_rent(request):
    user = request.user
    if user.is_authenticated:       
        rentals = Rental.objects.filter(client=user, closed=False) \
            .annotate(to6month=F('expired_at') + timedelta(days=180)) \
            .annotate(overprice=F('price') * 2)
             
        return render(request, 'my-rent.html', {'rentals': rentals})
    
    else:
        return redirect("/") 


def boxes(request):
    storages = Storage.objects.all().prefetch_related('boxes') \
        .annotate(box_min_price=Min(F('boxes__price'))) \
        .annotate(box_count=Count('boxes')) \
        .annotate(box_free=Count('boxes', filter=Q(boxes__busy=False)))
    
    return render(
        request,
        template_name="boxes.html",
        context={'storages': storages,
                 'boxes': boxes}
    )

def payment(request, pk):
    
    box = Box.objects.get(id=pk)
  
    description = f'Аренда склада № {box.id} по адресу: {box.storage} на один месяц'
    amount = box.price

    # Создайте экземпляр заказа и сохраните его в базе данных
    order = Order(
        user=request.user,
        box=box,
        description=description,
        amount=amount)
    order.save()

    # Создайте платеж в ЮKassa
    payment = create_payment(order.pk, amount, description, request.build_absolute_uri(reverse('payment_success', kwargs={'pk': order.pk})))
    order.payment_id = payment.id
    order.save()
 
    # Перенаправьте пользователя на страницу оплаты
    return redirect(payment.confirmation.confirmation_url)


# def create_selfstorage_order(request):
#     if request.method == 'POST':
#         # Получите данные из формы (или другого источника) и создайте новый заказ
#         description = request.POST['description']
#         amount = request.POST['amount']

#         # Создайте экземпляр заказа и сохраните его в базе данных
#         order = Order(user=request.user, description=description, amount=amount)
#         order.save()

#         # Создайте платеж в ЮKassa
#         payment = create_payment(order.pk, amount, request.build_absolute_uri(reverse('payment_success')))

#         # Перенаправьте пользователя на страницу оплаты
#         return redirect(payment.confirmation.confirmation_url)

#     return render(request, 'create_order.html')


def payment_success(request, pk):

    user = request.user
    if not user.is_authenticated:
        return redirect("/")   
    
    order = Order.objects.get(id=pk)
    status = get_payment_status(order.payment_id)
    print(status)
    if status == 'succeeded':
        # Найти заказ по payment_id и обновить его статус
        order = Order.objects.get(payment_id=order.payment_id)
        order.status = 'PAID'
        order.save()
        
        rental = Rental.objects.create(
            client=user,
            box=order.box,
            comment=f'Аренду успешно обновлена {now().date()}',
            expired_at=now() + timedelta(days=30),
            paid=True,
            price=order.box.price
        )
        send_email_payment_success(user.email)

    return redirect(reverse('my-rent'))
