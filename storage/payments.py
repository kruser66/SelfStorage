from yookassa import Configuration, Payment
from yookassa.domain.request import PaymentRequest
from django.conf import settings
import uuid


Configuration.configure(
    settings.YOOKASSA_SHOP_ID,
    settings.YOOKASSA_SECRET_KEY
)


def create_payment(order_id, amount, description, return_url):

    payment_data = {
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url
        },
        "capture": True,
        "description": description
    }

    payment = Payment.create(PaymentRequest(payment_data), str(uuid.uuid4()))

    return payment


def get_payment_status(payment_id):
    payment = Payment.find_one(payment_id)
    return payment.status
