from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .docs import urlpatterns as docs_urlpatterns
from .views.categories import CategoryViewSet
from .views.compilations import (
    CompliationSoloViewSet,
    ComplilationRedactorionListViewSet,
    ComplilationFavoriteListViewSet
)
from .views.countries import CountryViewSet
from .views.genres import GenreViewSet
from .views.movies import MoviesViewSet
from .views.users import (user_verify_email, favorite_genres,
                          user_registration, user_create_activate, login,
                          refresh)

v1_router = DefaultRouter()
v1_router.register('movies', MoviesViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('gangres', GenreViewSet)
v1_router.register('countries', CountryViewSet)
v1_router.register(
    'complilations/redactorion',
    ComplilationRedactorionListViewSet,
    basename="comp-redac"
)
v1_router.register(
    'complilations/favorite',
    ComplilationFavoriteListViewSet,
    basename="comp-favorite"
)

urlpatterns = [
    path('v1/auth/verify-email/', user_verify_email),
    path('v1/auth/user-registration/', user_registration),
    path('v1/auth/activation/<token>/', user_create_activate),
    path('v1/auth/login/', login),
    path('v1/auth/refresh/', refresh),
    path('v1/users/favorite-genres/', favorite_genres),
    path('docs/', include(docs_urlpatterns)),
    path('v1/', include(v1_router.urls)),

    path(
        'v1/complilations/<int:pk>/',
        CompliationSoloViewSet.as_view(),
        name="complilation"
    ),
    # path('', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
]
