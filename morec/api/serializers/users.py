from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from movies.models import Genre
from users.models import User


class UserVerifyEmailSerializer(serializers.ModelSerializer):
    """Сериализатор для проверки почты в db"""
    class Meta:
        model = User
        fields = ('email', 'password')


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей"""

    fav_genres = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects,
        required=False,
        many=True,
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'fav_genres')

    def validate(self, attrs):
        genres = attrs.pop('fav_genres', None)
        attrs = super().validate(attrs)
        attrs['fav_genres'] = genres
        return attrs

    def create(self, validated_data):
        genres = validated_data.pop('fav_genres', None)
        user = User.objects.create_user(**validated_data)
        if genres is not None:
            user.fav_genres.add(*genres)
        return user


class CustomUserSerializer(UserSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ('username', 'id', 'email', 'date_of_birth', 'sex')
