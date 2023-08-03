import datetime

import jwt
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response

from morec.settings import (JWT_REGISTRATION_TTL, SECRET_KEY, SITE_NAME,
                            EMAIL_HOST_USER)


def sending_mail(email):
    payload = {"exp": datetime.datetime.now(
        tz=datetime.timezone.utc) + datetime.timedelta(
        JWT_REGISTRATION_TTL), "email": email}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    subject = 'Восстановление пароля КиноТочка'
    message = (
        f'Для восстановления пароля перейдите по ссылке\n '
        f'{SITE_NAME}/v1/auth/password-recovery/{encoded_jwt}/\n'
        f'ссылка активна 1 час'
    )
    recipient = email
    send_mail(subject, message, EMAIL_HOST_USER, [recipient])
    return Response(status=status.HTTP_200_OK)