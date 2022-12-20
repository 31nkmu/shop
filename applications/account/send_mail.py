from django.core.mail import send_mail


def send_activation_link(email, activation_code):
    full_link = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    send_mail(
        'Activation link',
        full_link,
        'karimovbillal20002@gmail.com',
        [email],
    )


def send_code(email, activation_code):
    send_mail(
        'Активационный код для смены пароля',
        activation_code,
        'karimovbillal20002@gmail.com',
        [email]
    )
