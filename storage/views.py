from random import choice

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from storage.models import Storage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from storage.payments import create_payment
from .forms import AccountForm, CustomUserCreationForm, LoginForm
from django.core.exceptions import ValidationError
from django.db.models import Count, Min, F, Q

from .models import Order, User, Rental


def user_login(request):
    if request.method == "POST":
        email=request.POST['EMAIL']
        password=request.POST['PASSWORD']
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)    
            return redirect("/my-rent")
        
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
    pass


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
        # user.password=request.POST['PASSWORD_EDIT']
        user.save()
    return redirect("/my-rent")    
    
    

# ################## LOGIN ############################
    
# def register_user(request, *args, **kwargs):
#     user = request.user
#     if user.is_authenticated:
#         return HttpResponse(f"Вы уже зарегистрированы как {user.email}")

#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             user = authenticate(
#                 request,
#                 username=form.cleaned_data.get("email"),
#                 password=form.cleaned_data.get("password1"),
#             )
#             login(request, user)
#             destination = kwargs.get("next")
#             if destination:
#                 return redirect(destination)
#             return redirect("/")
#     else:
#         form = CustomUserCreationForm()
#     return render(request, "users/register.html", {"form": form})


# def login_user(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             print(cd)
#             user = authenticate(username=cd["email"], password=cd["password"])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect("/")
#                 else:
#                     form.add_error(None, ValidationError("Этот аккаунт отключен"))
#             else:
#                 form.add_error(None, ValidationError("Неверный email или пароль."))
#     else:
#         form = LoginForm()
#     return render(request, "users/login.html", {"form": form})


# @login_required(login_url="users:login")
# def account(request):
#     user = request.user
#     paid_orders = user.orders.filter(payments__is_paid=True)
#     if request.method == "POST":
#         form = AccountForm(request.POST)
#         if form.is_valid():
#             user.email = form.cleaned_data["email"]
#             user.phonenumber = form.cleaned_data["phonenumber"]
#             user.phonenumber = form.cleaned_data["phonenumber"]
#             user.set_password(form.cleaned_data["password"])
#             user.save()
#     else:
#         form = AccountForm()

#     context = {"user": user, "paid_orders": paid_orders, "form": form}
#     return render(request, "account.html", context)


# ################### PAGES ###########################
def index(request):
    storages = Storage.objects.all().prefetch_related('boxes') \
        .annotate(box_min_price=Min(F('boxes__price'))) \
        .annotate(box_count=Count('boxes')) \
        .annotate(box_free=Count('boxes', filter=Q(boxes__busy=False)))
        
    random_storage = choice(storages)
        
    return render(request, 'index.html', {"random_storage": random_storage})


def faq(request):
    return render(request, 'faq.html')


# @login_required(login_url="users:login")
def my_rent(request):
    user = request.user
    if user.is_authenticated:
        print(user.id)
        
        rentals = Rental.objects.filter(client=user, box__busy=True)
        print(rentals)
        
        return render(request, 'my-rent.html', {'rentals': rentals})
    else:
        return redirect("/") 
    # paid_orders = user.orders.filter(status='PAID')
    # if request.method == "POST":
    #     form = AccountForm(request.POST)
    #     if form.is_valid():
    #         user.email = form.cleaned_data["email"]
    #         user.phonenumber = form.cleaned_data["phonenumber"]
    #         user.set_password(form.cleaned_data["password"])
    #         user.save()
    # else:
    #     form = AccountForm()

    # context = {"user": user, "paid_orders": paid_orders, "form": form}
    # return render(request, 'my-rent.html', context)


def boxes(request):
    storages = Storage.objects.all().prefetch_related('boxes') \
        .annotate(box_min_price=Min(F('boxes__price'))) \
        .annotate(box_count=Count('boxes')) \
        .annotate(box_free=Count('boxes', filter=Q(boxes__busy=False)))

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
