import datetime

import jwt
from rest_framework import serializers

from morec.settings import JWT_ACCESS_TTL, JWT_REFRESH_TTL, SECRET_KEY
from movies.models import Genre
from users.models import User


class UserVerifyEmailSerializer(serializers.ModelSerializer):
    """Сериализатор для проверки почты в db"""
    class Meta:
        model = User
        fields = ('email',)


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей"""

    class Meta:
        model = User
        fields = ('email', 'password', 'fav_genres')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data['email']
        password = validated_data['password']
        error_msg = 'email or password are incorrect'
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError(error_msg)
            validated_data['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError(error_msg)

        return validated_data

    def create(self, validated_data):
        print(validated_data)
        print(validated_data['user'].id)
        print(type(validated_data['user'].id))
        user_id = str(validated_data['user'].id)
        access_payload = {
            'iss': 'backend-api',
            'user_id': user_id,
            'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=JWT_ACCESS_TTL),
            'type': 'access'
        }
        access = jwt.encode(access_payload, SECRET_KEY)
        print(jwt.decode(access, SECRET_KEY, algorithms=['HS256']))

        refresh_payload = {
            'iss': 'backend-api',
            'user_id': user_id,
            'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=JWT_REFRESH_TTL),
            'type': 'refresh'
        }
        refresh = jwt.encode(refresh_payload, SECRET_KEY)

        return {
            'access': access,
            'refresh': refresh
        }


class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        refresh_token = validated_data['refresh_token']
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY)
            if payload['type'] != 'refresh':
                error_msg = {'refresh_token': 'Token type is not refresh!'}
                raise serializers.ValidationError(error_msg)
            validated_data['payload'] = payload
        except jwt.ExpiredSignatureError:
            error_msg = {'refresh_token': 'Refresh token is expired!'}
            raise serializers.ValidationError(error_msg)
        except jwt.InvalidTokenError:
            error_msg = {'refresh_token': 'Refresh token is invalid!'}
            raise serializers.ValidationError(error_msg)

        return validated_data

    def create(self, validated_data):
        access_payload = {
            'iss': 'backend-api',
            'email': validated_data['payload']['email'],
            'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=JWT_ACCESS_TTL),
            'type': 'access'
        }
        access = jwt.encode(access_payload, SECRET_KEY)

        refresh_payload = {
            'iss': 'backend-api',
            'email': validated_data['payload']['email'],
            'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=JWT_REFRESH_TTL),
            'type': 'refresh'
        }
        refresh = jwt.encode(refresh_payload, SECRET_KEY)

        return {
            'access': access,
            'refresh': refresh
        }


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ('email', 'username', 'date_of_birth', 'sex')
        read_only_fields = 'email'


class FavoriteGenresSerializer(serializers.ModelSerializer):
    fav_genres = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects,
        required=False,
        many=True,
    )

    class Meta:
        model = User
        fields = ('id', 'fav_genres')
