from yookassa import Configuration, Payment
from yookassa.domain.request import PaymentRequest
from environs import Env

env = Env()
env.read_env()

Configuration.configure(env('YOOKASSA_SHOP_ID'), env('YOOKASSA_SECRET_KEY'))


def create_payment(order_id, amount, return_url):
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
        "description": f"Оплата заказа №{order_id}"
    }

    payment = Payment.create(PaymentRequest(payment_data))
    return payment
