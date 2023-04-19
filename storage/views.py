from django.shortcuts import redirect, render
from django.urls import reverse

from storage.models import Box, Order, Storage

from .payments import create_payment


def index(request):
    return render(request, 'index.html')


def faq(request):
    return render(request, 'faq.html')


def my_rent(request):
    return render(request, 'my-rent.html')


def my_rent_empty(request):
    return render(request, 'my-rent-empty.html')


def boxes(request):

    storages = Storage.objects.all()
    return render(
        request,
        template_name="boxes.html",
        context={'storages': storages}
    )


def create_selfstorage_order(request):
    if request.method == 'POST':
        # Получите данные из формы (или другого источника) и создайте новый заказ
        description = request.POST['description']
        amount = request.POST['amount']

        # Создайте экземпляр заказа и сохраните его в базе данных
        order = Order(user=request.user, description=description, amount=amount)
        order.save()

        # Создайте платеж в ЮKassa
        payment = create_payment(order.pk, amount, request.build_absolute_uri(reverse('payment_success')))

        # Перенаправьте пользователя на страницу оплаты
        return redirect(payment.confirmation.confirmation_url)

    return render(request, 'create_order.html')
