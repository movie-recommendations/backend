from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from movies.models import Genre
from users.models import User


class UserVerifyEmailSerializer(serializers.ModelSerializer):
    """Сериализатор для проверки почты в db"""
    class Meta:
        model = User
        fields = ('email', 'password')


class UserGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id',)


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей"""

    fav_genres = UserGenreSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'fav_genres')

    def create(self, validated_data):
        if 'fav_genres' not in self.initial_data:
            return User.objects.create(**validated_data)
        print('qwer1234')
        fav_genres = validated_data.pop('fav_genres')
        print(fav_genres)
        user = User.objects.create(**validated_data)
        for fav_genre in fav_genres:
            user.fav_genres.add(*fav_genres)
        return user


class CustomUserSerializer(UserSerializer):
    """Сериализатор для просмотра пользователей"""
    fav_genres = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'id', 'email', 'first_name',
                  'last_name', 'fav_genres')

    def get_is_fav_genres(self, obj):
        request = self.context.get('request')
        return request.user.is_authenticated and Genre.objects.filter(
            user=request.user, fav_genres=obj
        ).exists()
