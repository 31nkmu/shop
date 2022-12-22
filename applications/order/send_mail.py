from django.core.mail import send_mail


def send_activation_link(email, activation_code, title, price):
    full_link = f'Подтверди заказ на продукт {title} на сумму {price}' \
                f'\n\nhttp://localhost:8000/api/v1/order/confirm/{activation_code}'
    send_mail(
        'Order confirm by py24',
        full_link,
        'karimovbillal20002@gmail.com',
        [email],
    )
