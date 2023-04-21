from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


def send_email(subject, message, emails_lst):
    # subject = 'УВЕДОМЛЕНИЕ SelfStorage'
    # message = 'test'
    from_email = settings.ADMIN_EMAIL
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, emails_lst)
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        return HttpResponseRedirect("/")
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse("Make sure all fields are entered and valid.")