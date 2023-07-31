from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.filters import MoviesFilter
from api.serializers.movies import (MovieRateSerializer,
                                    MoviesDetailSerializer,
                                    MoviesListSerializer)
from movies.models import Movie, RatingMovie


class MoviesViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Movie.objects.prefetch_related('genres', 'ratings', 'countries', 'favorite_for')
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = MoviesFilter
    ordering_fields = ('view_count', 'rate_kinopoisk')
    actions_serializer = {
        'list': MoviesListSerializer,
        'retrieve': MoviesDetailSerializer,
        'newest': MoviesListSerializer,
        'rate': MovieRateSerializer,
    }

    def get_serializer_class(self):
        return self.actions_serializer.get(self.action, MoviesListSerializer)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        detail=False,
        filter_backends=(),
    )
    def newest(self, request):
        queryset = self.queryset.filter(
            premiere_date__lte=datetime.now().date(),
        ).order_by('-premiere_date')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        user = request.user
        movie = self.get_object()
        if request.method == 'POST':
            movie.favorite_for.add(user)
        else:
            movie.favorite_for.remove(user)
        return Response(status=200)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
    )
    def setwatch(self, request, pk):
        user = request.user
        movie = self.get_object()
        if request.method == 'POST':
            movie.need_to_see.add(user)
        else:
            movie.need_to_see.remove(user)
        return Response(status=200)

    @action(
        detail=True,
        methods=('post', 'put', 'delete'),
        permission_classes=(IsAuthenticated,),
    )
    def rate(self, request, pk):
        user = request.user
        movie = self.get_object()

        try:
            user_rate = RatingMovie.objects.get(user=user, movie=movie)
        except RatingMovie.DoesNotExist:
            user_rate = None

        if user_rate is None:
            if request.method == 'POST':
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=user, movie=movie)
                return Response(status=status.HTTP_201_CREATED)

            return Response(
                {'error': 'Не существует'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.method == 'DELETE':
            user_rate.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == 'PUT':
            serializer = self.get_serializer(
                data=request.data,
                instance=user_rate,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, movie=movie)
            return Response(status=status.HTTP_200_OK)

        return Response(
            {'error': 'Рейтинг уже оставлен ранее'},
            status=status.HTTP_400_BAD_REQUEST,
        )


    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,),
    )
    def rates(self, request):
        queryset = self.queryset.filter(
            favorite_for=True
        )
        serializer = self.get_serializer(
            queryset.values(), many=True
        )
        return Response(data=serializer.data)