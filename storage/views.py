from django.shortcuts import render
from storage.models import Storage, Box


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
        context={'storages': storages,}
    )
