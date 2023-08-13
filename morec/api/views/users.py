import datetime

import jwt
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.authentication.mail import sending_mail
from api.serializers.users import (ChangePasswordSerializer,
                                   CustomUserCreateSerializer,
                                   CustomUserSerializer,
                                   FavoriteGenresSerializer, LoginSerializer,
                                   PasswordRecoverySerializer,
                                   UserVerifyEmailSerializer)
from api.tasks import send_email
from morec.settings import (EMAIL_HOST_USER, JWT_REGISTRATION_TTL, SECRET_KEY,
                            SITE_NAME)
from users.models import User


@swagger_auto_schema(
    method='post',
    request_body=UserVerifyEmailSerializer,
    responses={400: 'errors', 200: 'OK'},
)
@api_view(['POST'])
def user_verify_email(request):
    serializer = UserVerifyEmailSerializer(data=request.data)
    if serializer.is_valid():
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=CustomUserCreateSerializer,
    responses={400: 'errors', 200: 'OK'},
)
@api_view(['POST'])
def user_registration(request):
    serializer = CustomUserCreateSerializer(data=request.data)
    if serializer.is_valid():
        payload = {"exp": datetime.datetime.now(
            tz=datetime.timezone.utc) + datetime.timedelta(
            JWT_REGISTRATION_TTL)}
        payload.update(serializer.data)
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        subject = 'Активация аккаунта КиноТочка'
        message = (
            f'Для завершения регистрации перейдите по ссылке\n '
            f'{SITE_NAME}/api/v1/auth/activation/{encoded_jwt}/\n'
            f'ссылка активна 1 час'
        )
        recipient = serializer.data['email']
        send_email.delay(subject, message, [recipient], EMAIL_HOST_USER)
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_create_activate(request, token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
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


@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={400: 'errors', 201: 'access: "some_token"'},
)
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        response_data = serializer.save()
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=PasswordRecoverySerializer,
    responses={400: 'errors', 200: 'OK'},
)
@api_view(['POST'])
def password_recovery(request):
    if request.user.is_authenticated:
        return sending_mail(request.user.email)
    serializer = PasswordRecoverySerializer(data=request.data)
    if serializer.is_valid():
        return sending_mail(serializer.data['email'])
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='put',
    request_body=ChangePasswordSerializer,
    responses={400: 'errors', 200: 'OK'},
)
@api_view(['PUT'])
def update_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        try:
            payload = jwt.decode(
                serializer.data.get('token'), SECRET_KEY, algorithms="HS256"
            )
            user = get_object_or_404(User, email=payload['email'])
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response(status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response(
                'Срок действия ссылки истек',
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersMe(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user


@swagger_auto_schema(
    method='put',
    request_body=FavoriteGenresSerializer,
    responses={400: 'errors', 201: FavoriteGenresSerializer, 403: 'error'},
)
@swagger_auto_schema(
    method='get',
    responses={200: FavoriteGenresSerializer, 403: 'error'},
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
