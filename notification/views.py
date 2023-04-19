from django.shortcuts import render
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


def send_email(request):
    subject = 'УВЕДОМЛЕНИЕ SelfStorage'
    message = 'test'
    from_email = 'selfstorage@kruser.site'
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ["kruser@yandex.ru"])
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        return HttpResponseRedirect("/")
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse("Make sure all fields are entered and valid.")