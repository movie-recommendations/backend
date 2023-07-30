import datetime

import jwt
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers.users import (UserVerifyEmailSerializer,
                                   FavoriteGenresSerializer,
                                   CustomUserCreateSerializer, LoginSerializer,
                                   RefreshSerializer)
from morec.settings import (SECRET_KEY, HOST, EMAIL_HOST_USER,
                            JWT_REGISTRATION_TTL)
from users.models import User


@api_view(['POST'])
def user_verify_email(request):
    serializer = UserVerifyEmailSerializer(data=request.data)
    if serializer.is_valid():
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_registration(request):
    serializer = CustomUserCreateSerializer(data=request.data)
    if serializer.is_valid():
        payload = {"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(JWT_REGISTRATION_TTL)}
        payload.update(serializer.data)
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        subject = 'Активация аккаунта КиноТочка'
        message = (
            f'Для завершения регистрации перейдите по ссылке\n '
            f'{HOST}/api/v1/auth/activation/{encoded_jwt}/\n'
            f'ссылка активна 1 час'
        )
        recipient = serializer.data['email']
        send_mail(subject, message, EMAIL_HOST_USER, [recipient])
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_create_activate(request, token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithm="HS256")
        serializer = CustomUserCreateSerializer(data=data)
        if serializer.is_valid():
            validated_data = serializer.data
            genres = validated_data.pop('fav_genres', None)
            user = User.objects.create_user(**validated_data, is_active=True)
            if genres is not None:
                user.fav_genres.add(*genres)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except jwt.ExpiredSignatureError:
        return Response(
            'Срок действия ссылки истек', status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def favorite_genres(request):
    user = request.user
    if request.method == 'PUT':
        serializer = FavoriteGenresSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer = FavoriteGenresSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        response_data = serializer.save()
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def refresh(request):
    serializer = RefreshSerializer(data=request.data)
    if serializer.is_valid():
        response_data = serializer.save()
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
